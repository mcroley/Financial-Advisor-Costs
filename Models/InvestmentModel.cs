using System;
using System.ComponentModel.DataAnnotations;

namespace FinancialAdvisorCosts.Models
{
    public class InvestmentModel
    {
        // Flag to determine if results should be displayed
        [ScaffoldColumn(false)]
        public bool IsCalculated { get; set; } = false;

        [Display(Name = "Initial Value ($)")]
        [DisplayFormat(DataFormatString = "{0:C0}", ApplyFormatInEditMode = true)]
        public long InitialValue { get; set; } = 1000000; // whole dollars only

        [Display(Name = "Annual Advisor Fee (%)")]
        [Range(0, 100, ErrorMessage = "Enter fee as whole number (e.g. 1 for 1%).")]
        public int FeePercentage { get; set; } = 1; // 1% as whole number

        [Display(Name = "Years")]
        [Range(1, 100)]
        public int Years { get; set; } = 15;

        [Display(Name = "Anticipated Annual Return (%)")]
        [Range(0, 100, ErrorMessage = "Enter return as whole number (e.g. 5 for 5%).")]
        public int AnnualReturn { get; set; } = 5; // 5% as whole number

        // integer rates used in percentage points; calculations use integer math scaled by 100

        // Note: AnnualReturn is entered as a whole-number percent (e.g. 5 for 5%).
        public long FutureValueNoFees
        {
            get
            {
                long v = (long)InitialValue;
                for (int i = 0; i < Years; i++)
                {
                    // multiply by (100 + AnnualReturn) then divide by 100, rounding
                    v = (v * (100 + AnnualReturn) + 50) / 100;
                }
                return v;
            }
        }

        public long PortfolioValueWithFees
        {
            get
            {
                long v = (long)InitialValue;
                for (int i = 0; i < Years; i++)
                {
                    // apply net rate = (100 + AnnualReturn - FeePercentage)
                    v = (v * (100 + AnnualReturn - FeePercentage) + 50) / 100;
                }
                return v;
            }
        }

        // Total loss relative to no-fee future value (includes direct fees + lost returns)
        public long TotalFeesPaid => FutureValueNoFees - PortfolioValueWithFees;

        // OpportunityCost kept for compatibility: represents the total loss (fees + lost returns)
        public long OpportunityCost => TotalFeesPaid;

        // Simple fees paid (initial value × fee % × years, no compounding)
        [Display(Name = "Simple fees paid")]
        [DisplayFormat(DataFormatString = "{0:C0}", ApplyFormatInEditMode = true)]
        public long SimpleFeesPaid => (long)((InitialValue * FeePercentage * Years + 50) / 100);

        // Compound loss: only the lost investment opportunity (EXCLUDES direct fees)
        [Display(Name = "Compound loss from annual fees")]
        [DisplayFormat(DataFormatString = "{0:C0}", ApplyFormatInEditMode = true)]
        public long CompoundLoss => (FutureValueNoFees - PortfolioValueWithFees) - SimpleFeesPaid;

        // Extra compound effect: alias for the compound loss (kept for compatibility)
        [Display(Name = "Lost returns on fees (compound effect)")]
        [DisplayFormat(DataFormatString = "{0:C0}", ApplyFormatInEditMode = true)]
        public long ExtraCompoundEffect => CompoundLoss;

        // Total advisor cost: direct fees paid + lost investment opportunity (compound loss)
        [Display(Name = "Total advisor cost")]
        [DisplayFormat(DataFormatString = "{0:C0}", ApplyFormatInEditMode = true)]
        public long TotalAdvisorCost => SimpleFeesPaid + CompoundLoss;

        // Actual value including missed opportunity (portfolio plus lost gains)
        [Display(Name = "Actual value (including missed opportunity)")]
        [DisplayFormat(DataFormatString = "{0:C0}", ApplyFormatInEditMode = true)]
        public long ActualValueIncludingMissedOpportunity => PortfolioValueWithFees + OpportunityCost;
    }
}
