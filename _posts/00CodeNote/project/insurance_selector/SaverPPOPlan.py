from BaseInsurancePlan import BaseInsurancePlan


class MetaSaverPPOPlan(BaseInsurancePlan):
    """Plan A: Saver PPO"""

    def __init__(self):
        super().__init__("Saver PPO")

        # In-network limits
        self.in_network_deductible = 1700
        self.in_network_oop_max = 2200

        # Out-of-network limits
        self.out_of_network_deductible = 1700
        self.out_of_network_oop_max = 4000

        # Coinsurance rates after deductible
        # Saver plan: 保险公司支付90%, 你支付10% (in-network)
        # Saver plan: 保险公司支付70%, 你支付30% (out-of-network)
        self.telehealth_coinsurance_in_network = 1.00  # 0% coinsurance after deductible
        self.telehealth_coinsurance_out_of_network = "Not Applicable"
        self.d_o_visit_coinsurance_in_network = 0.10  # 10% coinsurance after deductible
        self.d_o_visit_coinsurance_out_of_network = 0.30
        self.specialist_coinsurance_in_network = 0.10
        self.specialist_coinsurance_out_of_network = 0.30
        self.non_hospital_ray_lab_coinsurance_in_network = 0.10
        self.non_hospital_ray_lab_coinsurance_out_of_network = 0.30
        self.pt_coinsurance_in_network = 0.10  # 10% coinsurance after deductible
        self.pt_coinsurance_out_of_network = 0.30  # 30% coinsurance after deductible
        self.chiropractic_spinal_coinsurance_in_network = 0.10
        self.chiropractic_spinal_coinsurance_out_of_network = 0.30
        self.acupuncture_coinsurance_in_network = 0.10
        self.acupuncture_coinsurance_out_of_network = 0.30
        self.surgery_coinsurance = 0.00  # 0% after deductible (Meta covers 100%)

        # Copay
        # No copay for Saver plan
        # self.pt_copay = 0
        self.telehealth_copay_in_network = 0
        self.telehealth_copy_out_of_network = 0
        self.d_o_visit_copay_in_network = 0
        self.d_o_visit_copy_out_of_network = 0
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

        # Plan costs
        self.monthly_premium = 1081.89 / 12  # $1081.89/年
        self.annual_credit = 750  # Meta每年给$750补贴
