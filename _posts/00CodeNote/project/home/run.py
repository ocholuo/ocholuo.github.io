"""Mortgage amortization calculator with colored terminal output and chart export."""

from __future__ import annotations

import datetime
import logging
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

# ── ANSI palette ──────────────────────────────────────────────────────────────
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ── Colored logging ───────────────────────────────────────────────────────────
class ColorFormatter(logging.Formatter):
    _COLORS = {
        logging.DEBUG: CYAN,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: MAGENTA + BOLD,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self._COLORS.get(record.levelno, RESET)
        record.levelname = f"{color}{record.levelname:<8}{RESET}"
        return super().format(record)


def _build_logger(name: str) -> logging.Logger:
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColorFormatter("%(levelname)s %(message)s"))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


logger = _build_logger(__name__)


# ── Data models ───────────────────────────────────────────────────────────────
@dataclass
class PaymentScenario:
    """A named payment strategy applied on top of a base ``LoanConfig``.

    Attributes:
        label: Short identifier used in logs and output filenames, e.g. ``"A"``.
        extra_payments: Dict of ``{month: extra_principal}`` for this scenario.
        lump_sum_month: Month for a one-time lump-sum payment (overrides base).
        lump_sum_amount: Dollar amount of the one-time lump-sum payment.
        description: Optional human-readable description shown in logs.
    """

    label: str
    extra_payments: dict[int, float] = field(default_factory=dict)
    lump_sum_month: int = 0
    lump_sum_amount: float = 0.0
    description: str = ""


@dataclass
class LoanConfig:
    """Immutable loan parameters.

    Attributes:
        purchase_price: Full purchase price of the property.
        down_payment: Cash paid upfront.
        loan_amount: Principal borrowed (auto-derived as purchase_price - down_payment).
        annual_interest_rate: Decimal annual rate, e.g. 0.0675 for 6.75 %.
        loan_term_months: Total number of monthly payments (typically 360).
        monthly_payment: Auto-derived from loan_amount, rate, and term via the
            standard amortization formula:
            M = P · r(1+r)^n / ((1+r)^n − 1)
        lump_sum_month: Month number at which a one-time extra payment is made.
        lump_sum_amount: Dollar amount of the one-time extra payment.
        extra_payments: Dict mapping month → extra principal for that month,
            e.g. ``{12: 20_000, 24: 10_000}``.  Each entry is independent.
    """

    purchase_price: float
    down_payment: float
    annual_interest_rate: float
    loan_term_months: int
    lump_sum_month: int = 0
    lump_sum_amount: float = 0.0
    extra_payments: dict[int, float] = field(default_factory=dict)
    """Map of {month: extra_principal} for scheduled one-off extra payments."""
    loan_amount: float = field(init=False)
    monthly_payment: float = field(init=False)

    def __post_init__(self) -> None:
        self.loan_amount = self.purchase_price - self.down_payment
        r = self.monthly_rate
        n = self.loan_term_months
        # Standard fixed-rate amortization formula: M = P·r(1+r)^n / ((1+r)^n − 1)
        self.monthly_payment = self.loan_amount * r * (1 + r) ** n / ((1 + r) ** n - 1)

    @property
    def monthly_rate(self) -> float:
        return self.annual_interest_rate / 12


@dataclass
class MonthlyRow:
    """Computed values for a single amortization period.

    Attributes:
        month: 1-based month number.
        starting_balance: Balance before this month's payment.
        interest_payment: Interest portion of the payment.
        principal_payment: Principal portion of the payment.
        extra_payment: Any additional principal paid this month.
        ending_balance: Balance after all payments are applied.
    """

    month: int
    starting_balance: float
    interest_payment: float
    principal_payment: float
    extra_payment: float
    ending_balance: float

    @property
    def monthly_payment(self) -> float:
        return self.interest_payment + self.principal_payment


@dataclass
class AmortizationResult:
    """Full results of an amortization run.

    Attributes:
        rows: One ``MonthlyRow`` per amortized month.
        total_interest: Total interest paid over the life of the loan.
        total_cost: Principal + total interest.
        payoff_month: Month the loan was paid off (may be < loan_term_months).
    """

    rows: list[MonthlyRow]
    total_interest: float
    total_cost: float
    payoff_month: int


# ── Chart ─────────────────────────────────────────────────────────────────────
class AmortizationChart:
    """Renders a cumulative interest vs. principal line chart from an
    ``AmortizationResult`` and saves it as a PNG.

    The X axis shows ``MM/YY`` labels derived from the loan start date.
    The Y axis shows cumulative dollar amounts paid.

    Example::

        chart = AmortizationChart(result, start_date=datetime.date(2025, 3, 1))
        chart.save("amortization.png")
    """

    def __init__(
        self,
        result: AmortizationResult,
        start_date: datetime.date | None = None,
        loan_amount: float = 0.0,
    ) -> None:
        self.result = result
        self.start_date = start_date or datetime.date.today()
        self.loan_amount = loan_amount

    def save(self, output_path: str | Path = "amortization_chart.png") -> Path:
        """Build the chart and write it to *output_path*. Returns the path."""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.ticker as mticker
        except ImportError as exc:
            raise ImportError(
                "matplotlib is required for chart output. "
                "Install it with: pip install matplotlib"
            ) from exc

        output_path = Path(output_path)
        dates, cum_interest, cum_principal = self._build_series()

        # ── figure setup ──────────────────────────────────────────────────────
        fig, ax = plt.subplots(figsize=(14, 6))
        fig.patch.set_facecolor("#0f1117")
        ax.set_facecolor("#0f1117")

        # ── lines ─────────────────────────────────────────────────────────────
        ax.plot(
            dates,
            cum_interest,
            color="#e05252",
            linewidth=2.0,
            label="Cumulative Interest Paid",
        )
        ax.plot(
            dates,
            cum_principal,
            color="#52aee0",
            linewidth=2.0,
            label="Cumulative Principal Paid",
        )

        # total cost reference line
        if self.loan_amount:
            ax.axhline(
                self.loan_amount,
                color="#888888",
                linewidth=1.0,
                linestyle="--",
                label=f"Original Loan  ${self.loan_amount:,.0f}",
            )

        # crossover annotation: first month interest < principal in cumulative terms
        crossover = self._find_crossover(cum_interest, cum_principal)
        if crossover is not None:
            cx, cy = dates[crossover], cum_interest[crossover]
            ax.annotate(
                f"Interest < Principal\n{cx.strftime('%b %Y')}",
                xy=(cx, cy),
                xytext=(20, 20),
                textcoords="offset points",
                fontsize=8,
                color="#ffcc44",
                arrowprops=dict(arrowstyle="->", color="#ffcc44", lw=1.0),
            )

        # ── endpoint dots + labels on both lines ─────────────────────────────
        end_date = dates[-1]
        end_interest = cum_interest[-1]
        end_principal = cum_principal[-1]

        # dot on each line
        ax.scatter([end_date], [end_interest], color="#e05252", s=60, zorder=5)
        ax.scatter([end_date], [end_principal], color="#52aee0", s=60, zorder=5)

        # decide label offset direction to avoid overlap
        gap = abs(end_interest - end_principal)
        i_offset = (12, 6) if end_interest >= end_principal else (12, -18)
        p_offset = (12, -18) if end_interest >= end_principal else (12, 6)
        if gap < ax.get_ylim()[1] * 0.05:  # lines too close → stack vertically
            i_offset = (12, 10)
            p_offset = (12, -18)

        ax.annotate(
            f"${end_interest:,.0f}",
            xy=(end_date, end_interest),
            xytext=i_offset,
            textcoords="offset points",
            fontsize=8,
            color="#e05252",
            fontweight="bold",
            arrowprops=dict(arrowstyle="-", color="#e05252", lw=0.8),
        )
        ax.annotate(
            f"${end_principal:,.0f}",
            xy=(end_date, end_principal),
            xytext=p_offset,
            textcoords="offset points",
            fontsize=8,
            color="#52aee0",
            fontweight="bold",
            arrowprops=dict(arrowstyle="-", color="#52aee0", lw=0.8),
        )

        # ── X axis: MM/YY ticks every 12 months ──────────────────────────────
        tick_dates = [dates[i] for i in range(0, len(dates), 12)]
        ax.set_xticks(tick_dates)
        ax.set_xticklabels(
            [d.strftime("%m/%y") for d in tick_dates],
            rotation=45,
            ha="right",
            fontsize=8,
            color="#cccccc",
        )

        # ── Y axis: dollar formatting ─────────────────────────────────────────
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax.tick_params(axis="y", colors="#cccccc", labelsize=9)

        # ── grid, labels, legend ──────────────────────────────────────────────
        ax.grid(color="#2a2a2a", linewidth=0.6, linestyle="--")
        ax.set_xlabel("Date (MM/YY)", color="#aaaaaa", fontsize=10)
        ax.set_ylabel("Cumulative Amount ($)", color="#aaaaaa", fontsize=10)
        ax.set_title(
            "Mortgage Amortization  —  Cumulative Interest vs. Principal",
            color="#ffffff",
            fontsize=13,
            fontweight="bold",
            pad=14,
        )
        legend = ax.legend(
            fontsize=9, facecolor="#1c1f26", edgecolor="#444444", labelcolor="#dddddd"
        )

        for spine in ax.spines.values():
            spine.set_edgecolor("#333333")

        # ── final numbers box ─────────────────────────────────────────────────
        summary = (
            f"Total interest: ${self.result.total_interest:,.0f}\n"
            f"Total cost:     ${self.result.total_cost:,.0f}\n"
            f"Payoff:         month {self.result.payoff_month}"
        )
        ax.text(
            0.02,
            0.97,
            summary,
            transform=ax.transAxes,
            fontsize=8,
            verticalalignment="top",
            color="#cccccc",
            bbox=dict(
                boxstyle="round,pad=0.4",
                facecolor="#1c1f26",
                edgecolor="#444444",
                alpha=0.85,
            ),
        )

        plt.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"Chart saved → {CYAN}{output_path.resolve()}{RESET}")
        return output_path

    # ── helpers ───────────────────────────────────────────────────────────────

    def _build_series(
        self,
    ) -> tuple[list[datetime.date], list[float], list[float]]:
        """Return parallel lists of (date, cum_interest, cum_principal)."""
        dates: list[datetime.date] = []
        cum_interest: list[float] = []
        cum_principal: list[float] = []
        ci = cp = 0.0

        for row in self.result.rows:
            # advance start_date by row.month months
            d = _add_months(self.start_date, row.month)
            ci += row.interest_payment
            cp += row.principal_payment + row.extra_payment
            dates.append(d)
            cum_interest.append(ci)
            cum_principal.append(cp)

        return dates, cum_interest, cum_principal

    @staticmethod
    def _find_crossover(
        cum_interest: list[float], cum_principal: list[float]
    ) -> int | None:
        """Return the first index where cumulative principal >= cumulative interest."""
        for i, (ci, cp) in enumerate(zip(cum_interest, cum_principal)):
            if cp >= ci:
                return i
        return None


def _add_months(d: datetime.date, months: int) -> datetime.date:
    """Return *d* advanced by *months* calendar months."""
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(
        d.day,
        [
            31,
            29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ][month - 1],
    )
    return datetime.date(year, month, day)


# ── Calculator ────────────────────────────────────────────────────────────────
class MortgageCalculator:
    """Computes a full amortization schedule for a fixed-rate mortgage.

    Example::

        cfg = LoanConfig(
            purchase_price=940_000,
            down_payment=188_000,
            annual_interest_rate=0.0675,
            loan_term_months=360,
            monthly_payment=4825.57,
        )
        calc = MortgageCalculator(cfg)
        result = calc.run()
        calc.print_schedule(result)
    """

    _TABLE_HEADER = (
        "| Month | Starting Balance | Monthly Payment | Interest Payment "
        "| Principal Payment | Extra Payment | Ending Balance |"
    )
    _TABLE_SEP = (
        "| ----- | ---------------- | --------------- | ---------------- "
        "| ----------------- | ------------- | -------------- |"
    )

    def __init__(self, config: LoanConfig) -> None:
        self.cfg = config

    # ── public ────────────────────────────────────────────────────────────────

    def run(self) -> AmortizationResult:
        """Execute the amortization and return a structured result."""
        rows: list[MonthlyRow] = []
        total_interest = 0.0
        balance = self.cfg.loan_amount

        for row in self._iter_months(balance):
            rows.append(row)
            total_interest += row.interest_payment
            if row.ending_balance <= 0:
                break

        payoff_month = rows[-1].month
        total_cost = self.cfg.loan_amount + total_interest
        return AmortizationResult(
            rows=rows,
            total_interest=total_interest,
            total_cost=total_cost,
            payoff_month=payoff_month,
        )

    def print_schedule(
        self,
        result: AmortizationResult,
        chart_path: str | Path | None = "amortization_chart.png",
        start_date: datetime.date | None = None,
    ) -> None:
        """Print the full amortization table with colored year-end summaries.

        Args:
            result: Computed amortization data.
            chart_path: Where to save the PNG chart. Pass ``None`` to skip.
            start_date: Loan origination date for the X-axis labels (default: today).
        """
        self._log_config()

        print(f"\n{BOLD}{self._TABLE_HEADER}{RESET}")
        print(self._TABLE_SEP)

        yearly_interest = 0.0
        year = 0

        for row in result.rows:
            self._print_row(row)
            yearly_interest += row.interest_payment

            if row.month % 12 == 0:
                year += 1
                logger.info(
                    f"Year {year:>2} (month {row.month:>3})  "
                    f"interest this year: {YELLOW}${yearly_interest:>10,.2f}{RESET}  "
                    f"remaining balance: {MAGENTA}${row.ending_balance:>12,.2f}{RESET}"
                )
                yearly_interest = 0.0

        print()
        logger.info(
            f"{BOLD}Payoff month       : " f"{GREEN}{result.payoff_month}{RESET}"
        )
        logger.info(
            f"{BOLD}Total interest paid: "
            f"{RED}${result.total_interest:>12,.2f}{RESET}"
        )
        logger.info(
            f"{BOLD}Total cost of loan : " f"{RED}${result.total_cost:>12,.2f}{RESET}"
        )

        if chart_path is not None:
            AmortizationChart(
                result,
                start_date=start_date,
                loan_amount=self.cfg.loan_amount,
            ).save(chart_path)

    # ── private ───────────────────────────────────────────────────────────────

    def _iter_months(self, initial_balance: float) -> Iterator[MonthlyRow]:
        balance = initial_balance
        cfg = self.cfg

        for month in range(1, cfg.loan_term_months + 1):
            starting_balance = balance
            interest = balance * cfg.monthly_rate
            principal = cfg.monthly_payment - interest

            extra = self._extra_payment(month)
            if extra:
                level = (
                    logging.WARNING if month == cfg.lump_sum_month else logging.DEBUG
                )
                logger.log(
                    level,
                    f"Month {month:>3}: extra payment {YELLOW}${extra:,.2f}{RESET} applied",
                )

            ending = balance - principal - extra
            yield MonthlyRow(
                month=month,
                starting_balance=starting_balance,
                interest_payment=interest,
                principal_payment=principal,
                extra_payment=extra,
                ending_balance=ending,
            )
            balance = ending
            if ending <= 0:
                break

    def _extra_payment(self, month: int) -> float:
        cfg = self.cfg
        if month == cfg.lump_sum_month and cfg.lump_sum_amount:
            return cfg.lump_sum_amount
        return cfg.extra_payments.get(month, 0.0)

    def _print_row(self, row: MonthlyRow) -> None:
        low_balance = row.ending_balance < self.cfg.loan_amount * 0.20
        color = RED if low_balance else RESET
        print(
            f"{color}"
            f"| {row.month:5d} "
            f"| ${row.starting_balance:>16,.2f} "
            f"| ${row.monthly_payment:>15,.2f} "
            f"| ${row.interest_payment:>16,.2f} "
            f"| ${row.principal_payment:>17,.2f} "
            f"| ${row.extra_payment:>13,.2f} "
            f"| ${row.ending_balance:>14,.2f} |"
            f"{RESET}"
        )

    def _log_config(self) -> None:
        cfg = self.cfg
        logger.info(f"{BOLD}Mortgage Amortization Calculator{RESET}")
        logger.info(
            f"  Purchase price      : {CYAN}${cfg.purchase_price:>12,.2f}{RESET}"
        )
        logger.info(f"  Down payment        : {CYAN}${cfg.down_payment:>12,.2f}{RESET}")
        logger.info(f"  Loan amount         : {CYAN}${cfg.loan_amount:>12,.2f}{RESET}")
        logger.info(
            f"  Annual interest rate: {CYAN}{cfg.annual_interest_rate * 100:.3f}%{RESET}"
        )
        logger.info(
            f"  Term                : {CYAN}{cfg.loan_term_months} months{RESET}"
        )
        logger.info(
            f"  Monthly payment     : {CYAN}${cfg.monthly_payment:>12,.2f}{RESET}"
            f"  {RESET}(auto-computed){RESET}"
        )
        if cfg.lump_sum_amount:
            logger.info(
                f"  Lump-sum at month {cfg.lump_sum_month}: "
                f"{YELLOW}${cfg.lump_sum_amount:,.2f}{RESET}"
            )
        if cfg.extra_payments:
            total_extra = sum(cfg.extra_payments.values())
            logger.info(
                f"  Scheduled extra payments: {YELLOW}{len(cfg.extra_payments)} months, "
                f"total ${total_extra:,.2f}{RESET}"
            )
            for m, amt in sorted(cfg.extra_payments.items()):
                logger.debug(f"    month {m:>3}: {CYAN}${amt:,.2f}{RESET}")


# ── Consolidated chart ────────────────────────────────────────────────────────
class ConsolidatedAmortizationChart:
    """Overlays all scenarios on one chart.

    All scenarios are drawn as dashed lines except the **last** scenario,
    which uses solid lines. Each scenario has its own color pair (interest /
    principal). Endpoint dots and ``$`` labels are added for every scenario.

    Example::

        ConsolidatedAmortizationChart(
            scenarios=scenarios,
            results=results,
            start_date=datetime.date(2025, 3, 1),
            loan_amount=752_000,
        ).save("amortization_chart_consolidated.png")
    """

    # Color pairs (interest_color, principal_color) cycled across scenarios
    _PALETTE = [
        ("#e05252", "#5298e0"),  # red / blue
        ("#e09a52", "#52e0c0"),  # orange / teal
        ("#c45ce0", "#e0d452"),  # purple / yellow
        ("#52e06a", "#e05290"),  # green / pink
    ]

    def __init__(
        self,
        scenarios: list[PaymentScenario],
        results: dict[str, AmortizationResult],
        start_date: datetime.date | None = None,
        loan_amount: float = 0.0,
    ) -> None:
        self.scenarios = scenarios
        self.results = results
        self.start_date = start_date or datetime.date.today()
        self.loan_amount = loan_amount

    def save(
        self, output_path: str | Path = "amortization_chart_consolidated.png"
    ) -> Path:
        """Build and save the consolidated chart."""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.ticker as mticker
        except ImportError as exc:
            raise ImportError(
                "matplotlib is required for chart output. "
                "Install it with: pip install matplotlib"
            ) from exc

        output_path = Path(output_path)
        last_label = self.scenarios[-1].label

        fig, ax = plt.subplots(figsize=(16, 7))
        fig.patch.set_facecolor("#0f1117")
        ax.set_facecolor("#0f1117")

        all_dates: list = []

        for idx, scenario in enumerate(self.scenarios):
            result = self.results.get(scenario.label)
            if result is None:
                continue

            int_color, prin_color = self._PALETTE[idx % len(self._PALETTE)]
            is_last = scenario.label == last_label
            linestyle = "-" if is_last else "--"
            linewidth = 2.2 if is_last else 1.4
            alpha = 1.0 if is_last else 0.55
            suffix = " (solid)" if is_last else " (dashed)"

            dates, cum_interest, cum_principal = self._build_series(result)
            all_dates.extend(dates)

            ax.plot(
                dates,
                cum_interest,
                color=int_color,
                linewidth=linewidth,
                linestyle=linestyle,
                alpha=alpha,
                label=f"{scenario.label} — Interest{suffix}",
            )
            ax.plot(
                dates,
                cum_principal,
                color=prin_color,
                linewidth=linewidth,
                linestyle=linestyle,
                alpha=alpha,
                label=f"{scenario.label} — Principal{suffix}",
            )

            # ── crossover annotation (last scenario only, to keep chart clean)
            if is_last:
                crossover = self._find_crossover(cum_interest, cum_principal)
                if crossover is not None:
                    cx, cy = dates[crossover], cum_interest[crossover]
                    ax.annotate(
                        f"Interest < Principal\n{cx.strftime('%b %Y')}",
                        xy=(cx, cy),
                        xytext=(20, 20),
                        textcoords="offset points",
                        fontsize=8,
                        color="#ffcc44",
                        arrowprops=dict(arrowstyle="->", color="#ffcc44", lw=1.0),
                    )

            # ── endpoint dots + labels ────────────────────────────────────────
            end_date = dates[-1]
            end_i = cum_interest[-1]
            end_p = cum_principal[-1]

            ax.scatter(
                [end_date], [end_i], color=int_color, s=55, zorder=6, alpha=alpha
            )
            ax.scatter(
                [end_date], [end_p], color=prin_color, s=55, zorder=6, alpha=alpha
            )

            gap = abs(end_i - end_p)
            i_offset = (10, 6) if end_i >= end_p else (10, -18)
            p_offset = (10, -18) if end_i >= end_p else (10, 6)
            if gap < 30_000:
                i_offset = (10, 10)
                p_offset = (10, -18)

            label_alpha = 1.0 if is_last else 0.7
            ax.annotate(
                f"{scenario.label}: ${end_i:,.0f}",
                xy=(end_date, end_i),
                xytext=i_offset,
                textcoords="offset points",
                fontsize=7.5,
                color=int_color,
                fontweight="bold",
                alpha=label_alpha,
                arrowprops=dict(arrowstyle="-", color=int_color, lw=0.7),
            )
            ax.annotate(
                f"{scenario.label}: ${end_p:,.0f}",
                xy=(end_date, end_p),
                xytext=p_offset,
                textcoords="offset points",
                fontsize=7.5,
                color=prin_color,
                fontweight="bold",
                alpha=label_alpha,
                arrowprops=dict(arrowstyle="-", color=prin_color, lw=0.7),
            )

        # ── original loan reference ───────────────────────────────────────────
        if self.loan_amount:
            ax.axhline(
                self.loan_amount,
                color="#666666",
                linewidth=1.0,
                linestyle="--",
                label=f"Original Loan  ${self.loan_amount:,.0f}",
            )

        # ── X axis ticks ──────────────────────────────────────────────────────
        if all_dates:
            all_dates_sorted = sorted(set(all_dates))
            tick_dates = [
                all_dates_sorted[i] for i in range(0, len(all_dates_sorted), 12)
            ]
            ax.set_xticks(tick_dates)
            ax.set_xticklabels(
                [d.strftime("%m/%y") for d in tick_dates],
                rotation=45,
                ha="right",
                fontsize=8,
                color="#cccccc",
            )

        # ── Y axis ────────────────────────────────────────────────────────────
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
        ax.tick_params(axis="y", colors="#cccccc", labelsize=9)

        # ── chrome ────────────────────────────────────────────────────────────
        ax.grid(color="#2a2a2a", linewidth=0.6, linestyle="--")
        ax.set_xlabel("Date (MM/YY)", color="#aaaaaa", fontsize=10)
        ax.set_ylabel("Cumulative Amount ($)", color="#aaaaaa", fontsize=10)
        ax.set_title(
            "Mortgage Amortization  —  All Scenarios Consolidated\n"
            f"(dashed = earlier scenarios · solid = {last_label})",
            color="#ffffff",
            fontsize=13,
            fontweight="bold",
            pad=14,
        )
        for spine in ax.spines.values():
            spine.set_edgecolor("#333333")

        # ── summary box (all scenarios) ───────────────────────────────────────
        lines = []
        for s in self.scenarios:
            r = self.results.get(s.label)
            if r:
                total_extra = sum(row.extra_payment for row in r.rows)
                lines.append(
                    f"{s.label}: "
                    f"cost \\${r.total_cost:,.0f}  interest \\${r.total_interest:,.0f}  "
                    f"extra \\${total_extra:,.0f}  payoff m{r.payoff_month}"
                )
        ax.text(
            0.02,
            0.97,
            "\n".join(lines),
            transform=ax.transAxes,
            fontsize=7.5,
            verticalalignment="top",
            color="#cccccc",
            bbox=dict(
                boxstyle="round,pad=0.4",
                facecolor="#1c1f26",
                edgecolor="#444444",
                alpha=0.85,
            ),
        )

        # ── legend: anchored below the summary box to avoid overlap ──────────
        n_summary = len(lines)
        summary_height = 0.04 + n_summary * 0.052
        ax.legend(
            fontsize=8,
            facecolor="#1c1f26",
            edgecolor="#444444",
            labelcolor="#dddddd",
            loc="upper left",
            bbox_to_anchor=(0.02, 0.97 - summary_height - 0.015),
            bbox_transform=ax.transAxes,
        )

        plt.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"Consolidated chart saved → {CYAN}{output_path.resolve()}{RESET}")
        return output_path

    # ── helpers ───────────────────────────────────────────────────────────────

    def _build_series(
        self, result: AmortizationResult
    ) -> tuple[list[datetime.date], list[float], list[float]]:
        dates, cum_interest, cum_principal = [], [], []
        ci = cp = 0.0
        for row in result.rows:
            ci += row.interest_payment
            cp += row.principal_payment + row.extra_payment
            dates.append(_add_months(self.start_date, row.month))
            cum_interest.append(ci)
            cum_principal.append(cp)
        return dates, cum_interest, cum_principal

    @staticmethod
    def _find_crossover(
        cum_interest: list[float], cum_principal: list[float]
    ) -> int | None:
        for i, (ci, cp) in enumerate(zip(cum_interest, cum_principal)):
            if cp >= ci:
                return i
        return None


# ── Comparison runner ─────────────────────────────────────────────────────────
class MortgageComparison:
    """Runs multiple payment scenarios against the same base loan.

    Each scenario produces its own amortization table and chart saved as
    ``amortization_chart_{label}.png`` in *output_dir*.

    Example::

        base = LoanConfig(purchase_price=940_000, down_payment=188_000, ...)

        comparison = MortgageComparison(
            base_config=base,
            scenarios=[
                PaymentScenario("A", extra_payments={12: 10_000, 24: 10_000}),
                PaymentScenario("B", extra_payments={12: 20_000, 24: 20_000}),
                PaymentScenario("C", lump_sum_month=24, lump_sum_amount=100_000),
            ],
            start_date=datetime.date(2025, 3, 1),
            output_dir=".",
        )
        comparison.run_all()
    """

    def __init__(
        self,
        base_config: LoanConfig,
        scenarios: list[PaymentScenario],
        start_date: datetime.date | None = None,
        output_dir: str | Path = ".",
    ) -> None:
        self.base_config = base_config
        self.scenarios = scenarios
        self.start_date = start_date or datetime.date.today()
        self.output_dir = Path(output_dir)

    def run_all(self) -> dict[str, AmortizationResult]:
        """Run every scenario, print its schedule, save its chart.

        Returns a dict mapping label → ``AmortizationResult``.
        """
        results: dict[str, AmortizationResult] = {}
        for scenario in self.scenarios:
            logger.info(
                f"\n{BOLD}{'─' * 60}{RESET}\n"
                f"  Scenario {CYAN}{scenario.label}{RESET}"
                + (f"  —  {scenario.description}" if scenario.description else "")
            )
            cfg = self._apply_scenario(scenario)
            calc = MortgageCalculator(cfg)
            result = calc.run()
            chart_path = self.output_dir / f"amortization_chart_{scenario.label}.png"
            calc.print_schedule(
                result, chart_path=chart_path, start_date=self.start_date
            )
            results[scenario.label] = result

        self._log_comparison_summary(results)

        # ── consolidated chart ────────────────────────────────────────────────
        consolidated_path = self.output_dir / "amortization_chart_consolidated.png"
        ConsolidatedAmortizationChart(
            scenarios=self.scenarios,
            results=results,
            start_date=self.start_date,
            loan_amount=self.base_config.loan_amount,
        ).save(consolidated_path)

        return results

    # ── private ───────────────────────────────────────────────────────────────

    def _apply_scenario(self, scenario: PaymentScenario) -> LoanConfig:
        """Return a new LoanConfig with the scenario's payment fields substituted."""
        return LoanConfig(
            purchase_price=self.base_config.purchase_price,
            down_payment=self.base_config.down_payment,
            annual_interest_rate=self.base_config.annual_interest_rate,
            loan_term_months=self.base_config.loan_term_months,
            lump_sum_month=scenario.lump_sum_month or self.base_config.lump_sum_month,
            lump_sum_amount=scenario.lump_sum_amount
            or self.base_config.lump_sum_amount,
            extra_payments=scenario.extra_payments,
        )

    def _log_comparison_summary(self, results: dict[str, AmortizationResult]) -> None:
        logger.info(f"\n{BOLD}{'═' * 60}")
        logger.info(f"  Scenario Comparison Summary{RESET}")
        logger.info(f"{'─' * 60}")
        header = f"  {'Scenario':<10} {'Payoff Month':>12} {'Total Interest':>16} {'Total Cost':>14}"
        logger.info(f"{BOLD}{header}{RESET}")
        for label, res in results.items():
            logger.info(
                f"  {CYAN}{label:<10}{RESET}"
                f" {GREEN}{res.payoff_month:>12}{RESET}"
                f" {YELLOW}${res.total_interest:>14,.0f}{RESET}"
                f" {RED}${res.total_cost:>12,.0f}{RESET}"
            )
        logger.info(f"{'─' * 60}")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":

    # # PNC
    # # ── Shared loan parameters (same across all scenarios) ────────────────────
    # base = LoanConfig(
    #     purchase_price=940_000,
    #     down_payment=196_000,
    #     annual_interest_rate=0.0675,  # try 0.0625 or 0.04
    #     loan_term_months=360,
    # )

    # # ── Payment scenarios ─────────────────────────────────────────────────────
    # scenarios = [
    #     PaymentScenario(
    #         label="A",
    #         description="No extra payments (baseline)",
    #         extra_payments={},
    #     ),
    #     PaymentScenario(
    #         label="B",
    #         description="$10k–$20k alternating yearly extra",
    #         extra_payments={
    #             1: 1_000,
    #             4: 9_000,
    #             5: 500,
    #             8: 1_000,
    #         },
    #     ),
    #     # PaymentScenario(
    #     #     label="C",
    #     #     description="$30k flat yearly extra",
    #     #     extra_payments={m: 30_000 for m in range(12, 361, 12)},
    #     # ),
    # ]

    # # # USBANK
    # base = LoanConfig(
    #     purchase_price=940_000,
    #     down_payment=215_000,
    #     annual_interest_rate=0.05875,  # try 0.0625 or 0.04
    #     loan_term_months=240,
    # )
    # # ── Payment scenarios ─────────────────────────────────────────────────────
    # scenarios = [
    #     PaymentScenario(
    #         label="A",
    #         description="No extra payments (baseline)",
    #         extra_payments={},
    #     ),
    #     PaymentScenario(
    #         label="B",
    #         description="$10k–$20k alternating yearly extra",
    #         extra_payments={
    #             1: 1_000,
    #             3: 3_000,
    #             9: 2_000,
    #             16: 20_000,
    #             19: 10_000,
    #         },
    #     ),
    #     PaymentScenario(
    #         label="C",
    #         description="$30k flat yearly extra",
    #         extra_payments={
    #             1: 1_000,
    #             3: 3_000,
    #             9: 2_000,
    #             16: 20_000,
    #             19: 10_000,
    #             21: 30_000,
    #             26: 50_000,
    #             29: 50_000,
    #             35: 50_000,
    #             41: 50_000,
    #             47: 50_000,
    #             53: 50_000,
    #         },
    #     ),
    #     PaymentScenario(
    #         label="D",
    #         description="$30k flat yearly extra",
    #         extra_payments={
    #             1: 1_000,
    #             3: 3_000,
    #             9: 2_000,
    #             16: 20_000,
    #             19: 10_000,
    #             21: 30_000,
    #             26: 50_000,
    #             29: 50_000,
    #             35: 50_000,
    #             41: 50_000,
    #             # 47: 50_000,
    #             # 53: 50_000,
    #         },
    #     ),
    # ]

    # # # Re-Finance
    base = LoanConfig(
        purchase_price=940_000,
        down_payment=284_000,
        annual_interest_rate=0.053,  # try 0.0625 or 0.04
        loan_term_months=180,
    )
    # ── Payment scenarios ─────────────────────────────────────────────────────
    scenarios = [
        PaymentScenario(
            label="A",
            description="No extra payments (baseline)",
            extra_payments={},
        ),
        PaymentScenario(
            label="B",
            description="$10k–$20k alternating yearly extra",
            extra_payments={
                1: 50_000,
                10: 50_000,
            },
        ),
        PaymentScenario(
            label="C",
            description="$10k–$20k alternating yearly extra",
            extra_payments={
                1: 50_000,
                10: 50_000,
                20: 50_000,
                30: 50_000,
            },
        ),
        PaymentScenario(
            label="D",
            description="$10k–$20k alternating yearly extra",
            extra_payments={
                1: 50_000,
                10: 50_000,
                20: 50_000,
                30: 50_000,
                40: 50_000,
                50: 50_000,
            },
        ),
    ]

    MortgageComparison(
        base_config=base,
        scenarios=scenarios,
        start_date=datetime.date(2025, 3, 1),
        output_dir="./_posts/00CodeNote/project/home",
    ).run_all()
