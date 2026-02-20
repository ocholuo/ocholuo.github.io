class BaseInsurancePlan:
    """保险计划基类"""

    def __init__(self, plan_name):
        self.plan_name = plan_name

        # In-network limits
        self.in_network_deductible = 0
        self.in_network_oop_max = 0

        # Out-of-network limits
        self.out_of_network_deductible = 0
        self.out_of_network_oop_max = 0

        # Coinsurance rates (区分网络类型)
        self.telehealth_coinsurance_in_network = 0.00
        self.telehealth_coinsurance_out_of_network = "Not Applicable"
        self.d_o_visit_coinsurance_in_network = 0.00
        self.d_o_visit_coinsurance_out_of_network = 0.00
        self.specialist_coinsurance_in_network = 0.00
        self.specialist_coinsurance_out_of_network = 0.00
        self.non_hospital_ray_lab_coinsurance_in_network = 0.00
        self.non_hospital_ray_lab_coinsurance_out_of_network = 0.00
        self.pt_coinsurance_in_network = 0.0
        self.pt_coinsurance_out_of_network = 0.0
        self.chiropractic_spinal_coinsurance_in_network = 0.00
        self.chiropractic_spinal_coinsurance_out_of_network = 0.00
        self.acupuncture_coinsurance_in_network = 0.00
        self.acupuncture_coinsurance_out_of_network = 0.00
        self.surgery_coinsurance = 0.0

        # Copay (固定费用, 主要用于Plus PPO)
        # self.pt_copay = 0  # 每次PT的固定copay
        self.telehealth_copay_in_network = 0
        self.telehealth_copy_out_of_network = 0
        self.d_o_visit_copay_in_network = 0
        self.d_o_visit_copy_out_of_network = 0.30
        self.specialist_copay_in_network = 0
        self.specialist_copy_out_of_network = 0
        self.non_hospital_ray_lab_copay_in_network = 0
        self.non_hospital_ray_lab_copy_out_of_network = 0
        self.pt_copay_in_network = 0
        self.pt_copay_out_of_network = 0
        self.chiropractic_spinal_copay_in_network = 0
        self.chiropractic_spinal_copy_out_of_network = 0
        self.acupuncture_copay_in_network = 0
        self.acupuncture_copy_out_of_network = 0
        self.surgery_copy = 0

        # Tracking spent amounts
        self.in_network_spent = 0
        self.out_of_network_spent = 0

        # Plan costs (月费和年度补贴)
        self.monthly_premium = 0  # 每月保费
        self.annual_credit = 0  # Meta每年给的补贴

    def reset_spent(self):
        """重置已支付金额, 用于计算新的场景"""
        self.in_network_spent = 0
        self.out_of_network_spent = 0

    def update_spent(self, amount, network_type):
        """更新已支付金额"""
        if network_type == "out-of-network":
            self.out_of_network_spent += amount
        else:
            self.in_network_spent += amount

    def calculate_cost(
        self,
        service_type: str,
        visits: int,
        cost_per_visit: int,
        network_type: str = "out-of-network",
    ) -> dict:
        """
        计算医疗服务的总费用

        参数:
            service_type: 服务类型 ("PT", "Surgery", "Chiropractic" 等)
            visits: 就诊次数
            cost_per_visit: 每次费用
            network_type: "in-network" 或 "out-of-network"

        返回:
            dict: 包含详细计算过程和最终费用
        """
        total_billed = visits * cost_per_visit

        if network_type == "out-of-network":
            deductible = self.out_of_network_deductible
            oop_max = self.out_of_network_oop_max
            spent_so_far = self.out_of_network_spent
        else:
            deductible = self.in_network_deductible
            oop_max = self.in_network_oop_max
            spent_so_far = self.in_network_spent

        # 根据服务类型和网络类型获取 coinsurance rate 或 copay
        coinsurance_rate = self._get_coinsurance_rate(service_type, network_type)
        copay = self._get_copay(service_type, network_type)

        self.network_type = network_type
        self.coinsurance_rate = coinsurance_rate
        self.copay = copay

        # 计算逻辑
        remaining_deductible = max(0, deductible - spent_so_far)
        remaining_oop = max(0, oop_max - spent_so_far)

        breakdown = {
            "保险计划": self.plan_name,
            "服务类型": service_type,
            "总账单金额": total_billed,
            "网络类型": network_type,
            "已支付金额": spent_so_far,
            "剩余Deductible": remaining_deductible,
            "剩余Out-of-pocket Maximum": remaining_oop,
            "计算步骤": [],
        }

        amount_left = total_billed
        you_pay = 0

        if copay > 0:
            # 如果有 copay（Plus PPO的情况）
            # 先处理 deductible
            if remaining_deductible > 0:
                deductible_payment = min(amount_left, remaining_deductible)
                you_pay += deductible_payment
                amount_left -= deductible_payment
                breakdown["计算步骤"].append(
                    {
                        "步骤": "1. 支付Deductible",
                        "说明": f"在Deductible满足之前, 你需要支付全部费用",
                        "计算": f"min(${total_billed}, ${remaining_deductible}) = ${deductible_payment}",
                        "注意": f"对比 remaining_deductible {remaining_deductible} 和 amount_left {amount_left}",
                        "你支付": deductible_payment,
                    }
                )

            # Deductible满足后, 按copay计算剩余的visits
            if amount_left > 0:
                # 计算满足deductible后剩余的visits
                visits_after_deductible = int(amount_left / cost_per_visit)
                copay_total = copay * visits_after_deductible

                # 确保不超过 out-of-pocket maximum
                max_additional_payment = remaining_oop - you_pay
                if copay_total > max_additional_payment:
                    copay_total = max_additional_payment
                    breakdown["计算步骤"].append(
                        {
                            "步骤": "2. 支付Copay",
                            "说明": f"Deductible满足后, 剩余{visits_after_deductible}次PT, 每次copay ${copay}",
                            "计算": f"${copay} × {visits_after_deductible}次 = ${copay * visits_after_deductible}",
                            "注意": "但已达到Out-of-pocket Maximum限制",
                            "你支付": copay_total,
                        }
                    )
                else:
                    breakdown["计算步骤"].append(
                        {
                            "步骤": "2. 支付Copay",
                            "说明": f"Deductible满足后, 剩余{visits_after_deductible}次PT, 每次copay ${copay}",
                            "计算": f"${copay} × {visits_after_deductible}次 = ${copay_total}",
                            "你支付": copay_total,
                        }
                    )
                you_pay += copay_total
        else:
            # 没有copay的情况（Saver PPO）
            # Step 1: 先付 Deductible
            if remaining_deductible > 0:
                deductible_payment = min(amount_left, remaining_deductible)
                you_pay += deductible_payment
                amount_left -= deductible_payment

                # amount_left: 1500
                # remaining_deductible: 1700
                # deductible_payment: 1500
                # you_pay = 1500 + 0
                # amount_left = 1500 - 1500

                # amount_left: 2000
                # remaining_deductible: 1700
                # deductible_payment: 1700
                # you_pay = 1700 + 0
                # amount_left = 2000 - 1700

                breakdown["计算步骤"].append(
                    {
                        "步骤": "1. 支付Deductible",
                        "说明": f"在Deductible满足之前, 你需要支付全部费用",
                        "计算": f"min(${total_billed}, ${remaining_deductible}) = ${deductible_payment}",
                        "注意": f"对比 remaining_deductible {remaining_deductible} 和 amount_left {amount_left}",
                        "你支付": deductible_payment,
                    }
                )

            # Step 2: Deductible满足后, 付 Coinsurance
            if amount_left > 0:
                # 检查是否会超过 out-of-pocket maximum
                coinsurance_payment = amount_left * coinsurance_rate

                # 确保不超过 out-of-pocket maximum
                max_additional_payment = remaining_oop - you_pay
                if coinsurance_payment > max_additional_payment:
                    coinsurance_payment = max_additional_payment
                    breakdown["计算步骤"].append(
                        {
                            "步骤": f"2. 支付Coinsurance ({int(coinsurance_rate*100)}%)",
                            "说明": f"Deductible满足后, 剩余${amount_left}的{int(coinsurance_rate*100)}%",
                            "计算": f"${amount_left} × {int(coinsurance_rate*100)}% = ${amount_left * coinsurance_rate}",
                            "注意": "但已达到Out-of-pocket Maximum限制",
                            "你支付": coinsurance_payment,
                        }
                    )
                else:
                    breakdown["计算步骤"].append(
                        {
                            "步骤": f"2. 支付Coinsurance ({int(coinsurance_rate*100)}%)",
                            "说明": f"Deductible满足后, 剩余${amount_left:.2f}的{int(coinsurance_rate*100)}%",
                            "计算": f"${amount_left:.2f} × {int(coinsurance_rate*100)}% = ${coinsurance_payment:.2f}",
                            "你支付": coinsurance_payment,
                        }
                    )

                you_pay += coinsurance_payment

        breakdown["你总共支付"] = you_pay
        breakdown["保险公司支付"] = total_billed - you_pay

        # 在 calculate_cost 函数的末尾，return 之前添加：
        # 确保单次支付不会让你超过年度总上限
        actual_payment = min(you_pay, remaining_oop)

        # 如果发生了封顶，记录在 breakdown 里
        if actual_payment < you_pay:
            breakdown["计算步骤"].append(
                {
                    "步骤": "达到封顶",
                    "说明": "本次服务触发了年度 Out-of-pocket Maximum",
                    "你支付": actual_payment,
                }
            )
            you_pay = actual_payment

        return breakdown

    def _get_coinsurance_rate(self, service_type, network_type):
        """根据服务类型和网络类型返回对应的 coinsurance rate"""
        mapping = {
            "PT": (
                "pt_coinsurance_in_network",
                "pt_coinsurance_out_of_network",
            ),
            "SURGERY": (
                "surgery_coinsurance",
                "surgery_coinsurance",
            ),  # Surgery is usually flat
            "SPECIALIST": (
                "specialist_coinsurance_in_network",
                "specialist_coinsurance_out_of_network",
            ),
        }
        service = mapping.get(
            service_type.upper(),
            ("pt_coinsurance_in_network", "pt_coinsurance_out_of_network"),
        )
        attr_name = service[0] if network_type == "in-network" else service[1]
        coinsurance_rate = getattr(self, attr_name, 0.10)  # Default to 10% if not found
        return 0.0 if coinsurance_rate == "Not Applicable" else coinsurance_rate

    def _get_copay(self, service_type, network_type):
        """根据服务类型返回对应的 copay"""
        if service_type.upper() in ["PT", "PHYSICAL THERAPY"]:
            if network_type == "in-network":
                return self.pt_copay_in_network
            else:
                return self.pt_copay_out_of_network
        return 0

    def print_calculation(self, result):
        """打印计算结果"""
        print(f"\n【{result['保险计划']}】- 总账单 ${result['总账单金额']:.2f}")

        for step in result["计算步骤"]:
            print(f"  {step['说明']}: ${step['你支付']:.2f}")

        print(
            f"  → 医疗费用: ${result['你总共支付']:.2f} | 保险支付: ${result['保险公司支付']:.2f}"
        )
