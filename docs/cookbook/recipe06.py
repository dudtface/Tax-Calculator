import numpy as np
import taxcalc as tc


# begin adding/customizing tc.Calculator class methods and calcfunctions


@tc.iterate_jit(nopython=True)
def pseudo_COLR(e00200, MARS, c00100,
                COLR_rt, COLR_c, COLR_ps, COLR_prt,
                COLR_amount, iitax, combined):
    """
    Calculates pseudo Cost-of-Living Refund amount.
    Note this is simply meant to illustrate a Python programming technique;
    this function does NOT calculate the exact Cost-of-Living Refund amount.
    See setting of COLR parameters below in specify_pseudo_COLR_policy method.
    """
    # calculate pseudo refund amount
    COLR_amount = 1000.
    # reduce income & combined tax liability because it is a refundable credit
    iitax -= COLR_amount
    combined -= COLR_amount
    return (COLR_amount, iitax, combined)

# end new calcfunctions used by customized Calculator class


class Calculator(tc.Calculator):
    """
    Customized tc.Calculator class that inherits all tc.Calculator methods
    and calcfunctions, adding/overriding some to get desired customization.
    """
    def __init__(self, policy=None, records=None, verbose=False,
                 sync_years=True, consumption=None,
                 # new Calculator constructor argument used in customization
                 colr_active=False):
        # start with same class constructor arguments as tc.Calculator class
        super().__init__(policy=policy, records=records,
                         verbose=verbose, sync_years=sync_years,
                         consumption=consumption)
        # remember whether pseudo_COLR is active or not
        self.colr_active = colr_active

    def specify_pseudo_COLR_policy(self):
        """
        Specifies policy parameters for the COLR policy in the current_year.
        See use of these parameters above in the pseudo_COLR calcfunction.
        """
        # reform implementation year
        reform_year = 2020
        # specify dictionary of parameter names and values for reform_year
        pvalue = {
            # credit phase-in rate on earnings
            'COLR_rt': [1.0],
            # ceiling on refundable credit varies by filing-unit type, MARS
            'COLR_c': [4000.0, 8000.0, 4000.0, 4000.0, 4000.0],
            # credit phase-out start AGI level varies by filing-unit type, MARS
            'COLR_ps': [30000.0, 50000.0, 30000.0, 30000.0, 30000.0],
            # credit phase-out rate per dollar of AGI above COLR_ps level
            'COLR_prt': [0.2]
        }
        for name in pvalue:
            setattr(self.__policy, name, np.array(pvalue[name], np.float64))
        # set parameter values for self.current_year
        this_year = self.current_year
        if self.colr_active and this_year >= reform_year:
            # set inflation-indexed values of COLR_c and COLR_ps for this_year
            irates = self.__policy.inflation_rates()
            syr = tc.Policy.JSON_START_YEAR
            for name in ['COLR_c', 'COLR_ps']:
                value = getattr(self.__policy, name)
                for year in range(reform_year, this_year):
                    value *= (1.0 + irates[year - syr])
                setattr(self.__policy, name, value)
        else:
            # set pseudo COLR ceiling amount to zero
            zeros = [0.0, 0.0, 0.0, 0.0, 0.0]
            setattr(self.__policy, 'COLR_c', np.array(zeros, np.float64))

    def calc_all(self, zero_out_calc_vars=False):
        """
        Call all tax-calculation functions for the current_year.
        """
        tc.BenefitPrograms(self)
        self._calc_one_year(zero_out_calc_vars)
        tc.BenefitSurtax(self)
        tc.BenefitLimitation(self)
        tc.FairShareTax(self.__policy, self.__records)
        tc.LumpSumTax(self.__policy, self.__records)
        # specify new Records variable to hold pseudo COLR amount
        zeros = np.zeros(self.__records.array_length, dtype=np.float64)
        setattr(self.__records, 'COLR_amount', zeros)
        # specify new Policy parameters to characterize pseudo COLR policy
        self.specify_pseudo_COLR_policy()  # (see above)
        # call new function that calculates pseudo COLRefund amount
        pseudo_COLR(self.__policy, self.__records)  # (see above)
        tc.ExpandIncome(self.__policy, self.__records)
        tc.AfterTaxIncome(self.__policy, self.__records)

# end of customized Calculator class definition


# top-level logic of program that uses customized Calculator class

"""
# read an "old" reform file from Tax-Calculator website
# ("old" means the reform file is defined relative to pre-TCJA policy)
reforms_url = ('https://raw.githubusercontent.com/'
               'PSLmodels/Tax-Calculator/master/taxcalc/reforms/')

# specify reform dictionary for pre-TCJA policy
reform1 = tc.Policy.read_json_reform(reforms_url + '2017_law.json')

# specify reform dictionary for TCJA as passed by Congress in late 2017
reform2 = tc.Policy.read_json_reform(reforms_url + 'TCJA.json')

# specify Policy object for pre-TCJA policy
bpolicy = tc.Policy()
bpolicy.implement_reform(reform1, print_warnings=False, raise_errors=False)
assert not bpolicy.parameter_errors

# specify Policy object for TCJA reform relative to pre-TCJA policy
rpolicy = tc.Policy()
rpolicy.implement_reform(reform1, print_warnings=False, raise_errors=False)
assert not rpolicy.parameter_errors
rpolicy.implement_reform(reform2, print_warnings=False, raise_errors=False)
assert not rpolicy.parameter_errors
"""

bpolicy = tc.Policy()
rpolicy = tc.Policy()

# specify customized Calculator objects using bpolicy and rpolicy
recs = tc.Records.cps_constructor()
calc1 = Calculator(policy=bpolicy, records=recs, colr_active=False)
calc2 = Calculator(policy=rpolicy, records=recs, colr_active=True)

for cyr in range(2018, 2022 + 1):
    # advance to and calculate for specified cyr
    calc1.advance_to_year(cyr)
    calc1.calc_all()
    calc2.advance_to_year(cyr)
    calc2.calc_all()
    # extract weighted amounts
    iitax_funits = calc1.total_weight()
    iitax_reven1 = calc1.weighted_total('iitax')
    iitax_reven2 = calc2.weighted_total('iitax')
    colr_amount = calc2.weighted_total('COLR_amount')
    # print weighted amounts for cyr
    line = 'YEAR,NUM,ITAX1,ITAX2,COLR=  {}  {:.3f}  {:.3f}  {:.3f}  {:.3f}'
    print(line.format(
        cyr,
        iitax_funits * 1e-6,
        iitax_reven1 * 1e-9,
        iitax_reven2 * 1e-9,
        colr_amount * 1e-9
    ))
