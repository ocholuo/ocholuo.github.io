from BaseInsurancePlan import BaseInsurancePlan


class PlusPPOUHCPlan(BaseInsurancePlan):
    """Plan B: Plus PPO"""

    def __init__(self):
        super().__init__("Plus PPO")

        # In-network limits
        self.in_network_deductible = 300
        self.in_network_oop_max = 2200

        # Out-of-network limits
        self.out_of_network_deductible = 600
        self.out_of_network_oop_max = 4000

        # Coinsurance rates after deductible
        # Plus plan没有coinsurance，使用copay
        self.telehealth_coinsurance_in_network = 0.00  # 0% coinsurance after deductible
        self.telehealth_coinsurance_out_of_network = "Not Applicable"
        self.d_o_visit_coinsurance_in_network = 0.00  # 10% coinsurance after deductible
        self.d_o_visit_coinsurance_out_of_network = 0.00
        self.specialist_coinsurance_in_network = 0.00
        self.specialist_coinsurance_out_of_network = 0.00
        self.non_hospital_ray_lab_coinsurance_in_network = 0.00
        self.non_hospital_ray_lab_coinsurance_out_of_network = 0.00
        self.pt_coinsurance_in_network = 0.00  # 10% coinsurance after deductible
        self.pt_coinsurance_out_of_network = 0.00  # 30% coinsurance after deductible
        self.chiropractic_spinal_coinsurance_in_network = 0.00
        self.chiropractic_spinal_coinsurance_out_of_network = 0.00
        self.acupuncture_coinsurance_in_network = 0.00
        self.acupuncture_coinsurance_out_of_network = 0.00
        self.surgery_coinsurance = 0.00  # 0% after deductible (Meta covers 100%)

        # Copay for Plus plan
        # self.pt_copay = 30  # $30 copay per PT visit
        self.telehealth_copay_in_network = 0
        self.telehealth_copy_out_of_network = "Not Applicable"
        self.d_o_visit_copay_in_network = 20
        self.d_o_visit_copy_out_of_network = 0.30
        self.specialist_copay_in_network = 30
        self.specialist_copy_out_of_network = 0.30
        self.non_hospital_ray_lab_copay_in_network = 0.10
        self.non_hospital_ray_lab_copy_out_of_network = 0.30
        self.pt_copay_in_network = 30
        self.pt_copay_out_of_network = 30
        self.chiropractic_spinal_copay_in_network = 30
        self.chiropractic_spinal_copy_out_of_network = 0.30
        self.acupuncture_copay_in_network = 30
        self.acupuncture_copy_out_of_network = 0.30
        self.surgery_copy = 0.00  # 0% after deductible (Meta covers 100%)

        # Plan costs
        self.monthly_premium = 1767.15 / 12  # $1767.15/年
        self.annual_credit = 0  # PPO没有年度补贴
