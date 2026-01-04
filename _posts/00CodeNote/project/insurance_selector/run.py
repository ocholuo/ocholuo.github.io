"""
健康保险费用计算器
Insurance Cost Calculator

支持两种保险计划:
- Plan A: Meta Saver Plan
- Plan B: PPO Plan

第一关: Deductible(自付额阶段)—— “填坑”
        这是保险生效前的“门槛”。
        逻辑:  在你支付的钱达到 deductible 之前, 保险公司一分钱都不出。
        脚本中的体现:  * 代码先计算 remaining_deductible(剩余还没填满的坑)。
                    如果账单金额小于这个坑, 你就得全额支付。
                    这个过程会一直持续到 remaining_deductible 变为 0。

第二关: Coinsurance / Copay(共同保险阶段)—— “打折”
        一旦你填满了 Deductible 的坑, 保险就开始介入了, 这时候你进入了“比例付费”阶段。
        逻辑:
            Saver Plan (HDHP): 走的是 Coinsurance 比例。比如 10%, 意味着账单打 1 折, 你付 10%, 保险付 90%。
            Plus Plan: 走的是 Copay 固定金额。比如无论诊费多贵, 你只付固定的 $25。
        脚本中的体现:
            代码判断 amount_left(满足免赔额后剩下的账单)。
            乘以 coinsurance_rate(如 0.10)或者加上固定 copay。

第三关: Out-of-Pocket Maximum (OOP Max) —— “封顶保护”
        这是为了防止你破产的最后防线。
        逻辑:  在一个年度内, 只要你自费的总额(Deductible + Coinsurance)达到了 oop_max 这个值, 剩下的所有医疗费用由保险公司 100% 承担。
        脚本中的体现:
            代码计算 remaining_oop(距离封顶线还有多远)。
            在计算 Coinsurance 或 Copay 时, 它会做一个 if 判断: 如果计算出来的钱超过了 remaining_oop, 那么你只需支付到封顶线为止。

举个例子(以 Saver Plan 为例):
假设你的 Deductible 是 $1,700, OOP Max 是 $2,200, Coinsurance 是 10%。
你有一张 $2,000 的账单:

第一阶段 (Deductible):
- 你要先填满 $1,700 的坑。
- 你支付: $1,700, 账单还剩 $300。

第二阶段 (Coinsurance):
- 剩余的 $300 按 10% 计算。
- $300 x 10% = $30。
- 你支付: $30。

第三阶段 (检查 OOP Max):
- 此时你总共付了 $1,700 + $30 = $1,730。
- 还没到 $2,200 的封顶线, 所以计算结束。

最终你付: $1,730。
"""

import logging
import os
import sys

# Constants
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[39m"

LOG_LEVEL = os.environ.get("My_App", "INFO")
logging.basicConfig(
    stream=sys.stdout,
    level=LOG_LEVEL,
    format="%(lineno)d:%(levelname)s:%(name)s:%(message)s",
)
logger = logging.getLogger(__name__)


from PlusPPOUHCPlan import PlusPPOUHCPlan
from SaverPPOPlan import MetaSaverPPOPlan


def calculate_annual_total_cost(plan, medical_cost):
    """
    计算年度总成本 (包括保费、医疗费用、减去补贴)

    参数:
        plan: 保险计划实例
        medical_cost: 医疗费用 (你需要支付的部分)

    返回:
        dict: 包含详细的年度成本分解
    """
    annual_premium = plan.monthly_premium * 12
    net_annual_cost = annual_premium + medical_cost - plan.annual_credit

    return {
        "保险计划": plan.plan_name,
        "月保费": plan.monthly_premium,
        "年保费总计": annual_premium,
        "医疗费用": medical_cost,
        "年度补贴": plan.annual_credit,
        "年度净成本": net_annual_cost,
    }


def print_annual_cost(cost_breakdown):
    """打印年度成本分解"""
    parts = [f"保费 ${cost_breakdown['年保费总计']:.2f}"]
    if cost_breakdown["年度补贴"] > 0:
        parts.append(f"补贴 -${cost_breakdown['年度补贴']:.2f}")
    logger.info(
        f"  → 年度成本: ${cost_breakdown['年度净成本']:.2f} ({' + '.join(parts)})"
    )


def compare_plans_annual_cost(
    service_type, visits, cost_per_visit, network_type="out-of-network"
):
    """
    比较两种保险计划的年度总成本

    参数:
        service_type: 服务类型
        visits: 就诊次数
        cost_per_visit: 每次费用
        network_type: 网络类型
    """
    logger.info("\n" + "=" * 60)
    logger.info(
        f"保险计划对比: {visits}次{service_type} × ${cost_per_visit} ({network_type})"
    )
    logger.info("=" * 60)

    # Plan A: Saver PPO
    plan_a = MetaSaverPPOPlan()
    result_a = plan_a.calculate_cost(service_type, visits, cost_per_visit, network_type)
    logger.info(result_a)

    plan_a.print_calculation(result_a)

    # 计算 Plan A 年度总成本
    annual_cost_a = calculate_annual_total_cost(plan_a, result_a["你总共支付"])
    print_annual_cost(annual_cost_a)

    # Plan B: Plus PPO
    plan_b = PlusPPOUHCPlan()
    result_b = plan_b.calculate_cost(service_type, visits, cost_per_visit, network_type)
    plan_b.print_calculation(result_b)

    # 计算 Plan B 年度总成本
    annual_cost_b = calculate_annual_total_cost(plan_b, result_b["你总共支付"])
    print_annual_cost(annual_cost_b)

    # 比较结果
    logger.info("\n" + "-" * 60)
    savings = annual_cost_a["年度净成本"] - annual_cost_b["年度净成本"]
    if savings > 0:
        logger.info(f"💰 推荐: Plus PPO (节省 ${savings:.2f}/年)")
    elif savings < 0:
        logger.info(f"💰 推荐: Saver PPO (节省 ${-savings:.2f}/年)")
    else:
        logger.info("两种计划年度成本相同")
    logger.info("=" * 60)


def compare_plans_multiple_services(services):
    """
    比较两种保险计划的年度总成本 - 支持多个医疗服务

    参数:
        services: 医疗服务列表, 每个服务是一个dict, 包含:
            - service_type: 服务类型
            - visits: 就诊次数
            - cost_per_visit: 每次费用
            - network_type: 网络类型 (可选, 默认"out-of-network")

    示例:
        services = [
            {"service_type": "PT", "visits": 50, "cost_per_visit": 70, "network_type": "out-of-network"},
            {"service_type": "PT", "visits": 10, "cost_per_visit": 70, "network_type": "in-network"},
        ]
    """
    logger.info("=" * 60)
    logger.info(f"{GREEN}保险计划对比 - 多项医疗服务{RESET}")
    logger.info("=" * 60)

    # 初始化两个计划
    plan_a = MetaSaverPPOPlan()
    plan_b = PlusPPOUHCPlan()

    total_medical_a = 0
    total_medical_b = 0

    # 逐项计算每个服务
    for i, service in enumerate(services, 1):
        service_type = service.get("service_type", "PT")
        visits = service.get("visits", 0)
        cost_per_visit = service.get("cost_per_visit", 0)
        network_type = service.get("network_type", "out-of-network")

        logger.info(
            f"服务 {i}: {visits}次{service_type} × ${cost_per_visit} ({network_type})\n"
        )

        # 计算 Plan A
        result_a = plan_a.calculate_cost(
            service_type, visits, cost_per_visit, network_type
        )
        total_medical_a += result_a["你总共支付"]
        plan_a.update_spent(result_a["你总共支付"], network_type)
        logger.info(f"  Saver PPO: ${result_a['你总共支付']:.2f}")
        logger.info(f"  - network_type: {YELLOW}{plan_a.network_type}{RESET}")
        logger.info(f"  - coinsurance_rate: {YELLOW}{plan_a.coinsurance_rate}{RESET}")
        logger.info(f"  - copay: {YELLOW}{plan_a.copay}{RESET}\n")

        # 计算 Plan B
        result_b = plan_b.calculate_cost(
            service_type, visits, cost_per_visit, network_type
        )
        total_medical_b += result_b["你总共支付"]
        plan_b.update_spent(result_b["你总共支付"], network_type)
        logger.info(f"  Plus PPO: ${result_b['你总共支付']:.2f}")
        logger.info(f"  - network_type: {YELLOW}{plan_b.network_type}{RESET}")
        logger.info(f"  - coinsurance_rate: {YELLOW}{plan_b.coinsurance_rate}{RESET}")
        logger.info(f"  - copay: {YELLOW}{plan_b.copay}{RESET}\n")

        # logger.info(f"  Saver PPO: {result_a}")
        for result in [result_a, result_b]:
            logger.info(f"Plan: {MAGENTA}{result['保险计划']}{RESET}")
            for step in result["计算步骤"]:
                logger.info(f"{step['步骤']}")
                logger.info(f"- {step['说明']}")
                logger.info(f"- {step['计算']}")
                logger.info(f"- {step['你支付']}\n")
                # for k, v in step.items():
                #     logger.info(f"- {k}: {YELLOW}{v}{RESET}")

    # 计算年度总成本
    logger.info("-" * 60)
    logger.info(f"{GREEN}年度总成本汇总{RESET}")
    logger.info("-" * 60)

    annual_cost_a = calculate_annual_total_cost(plan_a, total_medical_a)
    logger.info(f"【Saver PPO】")
    logger.info(f"  医疗费用: ${total_medical_a:.2f}")
    logger.info(f"  年度保费: ${annual_cost_a['年保费总计']:.2f}")
    if annual_cost_a["年度补贴"] > 0:
        logger.info(f"  Meta补贴: -${annual_cost_a['年度补贴']:.2f}")
    logger.info(f"  → 年度总成本: ${annual_cost_a['年度净成本']:.2f}")

    annual_cost_b = calculate_annual_total_cost(plan_b, total_medical_b)
    logger.info(f"【Plus PPO】")
    logger.info(f"  医疗费用: ${total_medical_b:.2f}")
    logger.info(f"  年度保费: ${annual_cost_b['年保费总计']:.2f}")
    logger.info(f"  → 年度总成本: ${annual_cost_b['年度净成本']:.2f}")

    # 比较结果
    logger.info("-" * 60)
    savings = annual_cost_a["年度净成本"] - annual_cost_b["年度净成本"]
    if savings > 0:
        logger.info(f"💰 推荐: Plus PPO (节省 ${savings:.2f}/年)")
    elif savings < 0:
        logger.info(f"💰 推荐: Saver PPO (节省 ${-savings:.2f}/年)")
    else:
        logger.info("两种计划年度成本相同")
    logger.info("=" * 60)


if __name__ == "__main__":
    # 示例 1: 单个服务
    # compare_plans_annual_cost(
    #     service_type="PT", visits=50, cost_per_visit=70, network_type="out-of-network"
    # )

    # 示例 2: 多个医疗服务
    services = [
        # {
        #     "service_type": "PT",
        #     "visits": 1,
        #     "cost_per_visit": 70,
        #     "network_type": "out-of-network",
        # },
        {
            "service_type": "PT",
            "visits": 50,
            "cost_per_visit": 70,
            "network_type": "out-of-network",
        },
        # {
        #     "service_type": "PT",
        #     "visits": 50,
        #     "cost_per_visit": 70,
        #     "network_type": "in-network",
        # },
    ]
    compare_plans_multiple_services(services)
