import numpy as np
import scipy.stats as stats
from scipy.stats import chi2
import math

class StatisticsCalculator:
    """
    Statistical calculation utilities for diagnostic test performance analysis.
    Implements MedCalc and GraphPad style calculations for nucleic acid amplification techniques.
    """
    
    def __init__(self):
        pass
    
    def calculate_diagnostic_stats(self, tp, fn, tn, fp):
        """
        Calculate comprehensive diagnostic statistics with 95% confidence intervals.
        
        Args:
            tp (int): True Positives
            fn (int): False Negatives
            tn (int): True Negatives
            fp (int): False Positives
            
        Returns:
            dict: Dictionary containing all calculated statistics with confidence intervals
        """
        # Basic calculations
        total = tp + fn + tn + fp
        
        # Sensitivity (True Positive Rate)
        sensitivity = (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 0
        sensitivity_ci = self._wilson_ci(tp, tp + fn)
        
        # Specificity (True Negative Rate)
        specificity = (tn / (tn + fp)) * 100 if (tn + fp) > 0 else 0
        specificity_ci = self._wilson_ci(tn, tn + fp)
        
        # Positive Predictive Value (Precision)
        ppv = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 0
        ppv_ci = self._wilson_ci(tp, tp + fp)
        
        # Negative Predictive Value
        npv = (tn / (tn + fn)) * 100 if (tn + fn) > 0 else 0
        npv_ci = self._wilson_ci(tn, tn + fn)
        
        # Accuracy
        accuracy = ((tp + tn) / total) * 100 if total > 0 else 0
        accuracy_ci = self._wilson_ci(tp + tn, total)
        
        return {
            'sensitivity': sensitivity,
            'sensitivity_ci': [sensitivity_ci[0] * 100, sensitivity_ci[1] * 100],
            'specificity': specificity,
            'specificity_ci': [specificity_ci[0] * 100, specificity_ci[1] * 100],
            'ppv': ppv,
            'ppv_ci': [ppv_ci[0] * 100, ppv_ci[1] * 100],
            'npv': npv,
            'npv_ci': [npv_ci[0] * 100, npv_ci[1] * 100],
            'accuracy': accuracy,
            'accuracy_ci': [accuracy_ci[0] * 100, accuracy_ci[1] * 100],
            'tp': tp,
            'fn': fn,
            'tn': tn,
            'fp': fp,
            'total': total
        }
    
    def _wilson_ci(self, successes, trials, confidence=0.95):
        """
        Calculate Wilson confidence interval for proportions.
        More accurate than normal approximation for small samples.
        
        Args:
            successes (int): Number of successes
            trials (int): Total number of trials
            confidence (float): Confidence level (default 0.95)
            
        Returns:
            tuple: (lower_bound, upper_bound)
        """
        if trials == 0:
            return (0, 0)
        
        z = stats.norm.ppf(1 - (1 - confidence) / 2)
        p = successes / trials
        n = trials
        
        denominator = 1 + z**2 / n
        centre = (p + z**2 / (2 * n)) / denominator
        half_width = z * math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denominator
        
        return (max(0, centre - half_width), min(1, centre + half_width))
    
    def calculate_cohens_kappa(self, tech1_data, tech2_data):
        """
        Calculate Cohen's Kappa statistic with 95% confidence intervals.
        Simulates agreement analysis between two techniques.
        
        Args:
            tech1_data: Performance data for technique 1
            tech2_data: Performance data for technique 2
            
        Returns:
            dict: Kappa value with confidence intervals
        """
        # Simulate agreement matrix based on performance metrics
        # This is a simplified simulation for demonstration
        
        # Extract performance metrics
        sens1 = tech1_data['Sensitivity (%)'] / 100
        spec1 = tech1_data['Specificity (%)'] / 100
        sens2 = tech2_data['Sensitivity (%)'] / 100
        spec2 = tech2_data['Specificity (%)'] / 100
        
        # Simulate observed agreement
        # Higher agreement when performance metrics are similar
        agreement_positive = min(sens1, sens2)
        agreement_negative = min(spec1, spec2)
        
        # Calculate overall observed agreement (simplified)
        po = (agreement_positive + agreement_negative) / 2
        
        # Calculate expected agreement by chance
        # Simplified calculation based on marginal probabilities
        pe = ((sens1 + sens2) / 2) * 0.5 + ((spec1 + spec2) / 2) * 0.5
        
        # Cohen's Kappa
        kappa = (po - pe) / (1 - pe) if (1 - pe) != 0 else 0
        
        # Simplified confidence interval calculation
        # In practice, this would use more complex variance calculations
        se_kappa = math.sqrt(po * (1 - po) / 100)  # Simplified standard error
        z_score = 1.96  # 95% CI
        
        ci_lower = kappa - z_score * se_kappa
        ci_upper = kappa + z_score * se_kappa
        
        return {
            'kappa': kappa,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'observed_agreement': po,
            'expected_agreement': pe
        }
    
    def interpret_kappa(self, kappa_value):
        """
        Interpret Cohen's Kappa value according to standard guidelines.
        
        Args:
            kappa_value (float): Kappa coefficient
            
        Returns:
            str: Interpretation string
        """
        if kappa_value < 0:
            return "Poor agreement (worse than chance)"
        elif kappa_value < 0.20:
            return "Slight agreement"
        elif kappa_value < 0.40:
            return "Fair agreement"
        elif kappa_value < 0.60:
            return "Moderate agreement"
        elif kappa_value < 0.80:
            return "Substantial agreement"
        else:
            return "Almost perfect agreement"
    
    def mcnemar_test_simulation(self, tech1_data, tech2_data):
        """
        Simulate McNemar's test for comparing paired binary outcomes.
        
        Args:
            tech1_data: Performance data for technique 1
            tech2_data: Performance data for technique 2
            
        Returns:
            dict: Test results including p-value
        """
        # Simulate discordant pairs based on performance differences
        sens_diff = abs(tech1_data['Sensitivity (%)'] - tech2_data['Sensitivity (%)'])
        spec_diff = abs(tech1_data['Specificity (%)'] - tech2_data['Specificity (%)'])
        
        # Simulate discordant pairs (simplified)
        # In reality, this would be based on actual paired observations
        b = max(1, int(sens_diff * 0.1))  # Technique 1 positive, Technique 2 negative
        c = max(1, int(spec_diff * 0.1))  # Technique 1 negative, Technique 2 positive
        
        # McNemar's test statistic
        if (b + c) > 0:
            chi_square = ((abs(b - c) - 1) ** 2) / (b + c)
            p_value = 1 - chi2.cdf(chi_square, df=1)
        else:
            chi_square = 0
            p_value = 1.0
        
        return {
            'chi_square': chi_square,
            'p_value': p_value,
            'discordant_pairs_b': b,
            'discordant_pairs_c': c
        }
    
    def calculate_likelihood_ratios(self, sensitivity, specificity):
        """
        Calculate positive and negative likelihood ratios.
        
        Args:
            sensitivity (float): Sensitivity percentage
            specificity (float): Specificity percentage
            
        Returns:
            dict: Likelihood ratios
        """
        sens = sensitivity / 100
        spec = specificity / 100
        
        # Positive Likelihood Ratio
        plr = sens / (1 - spec) if (1 - spec) > 0 else float('inf')
        
        # Negative Likelihood Ratio
        nlr = (1 - sens) / spec if spec > 0 else float('inf')
        
        return {
            'positive_lr': plr,
            'negative_lr': nlr
        }
    
    def diagnostic_odds_ratio(self, tp, fn, tn, fp):
        """
        Calculate diagnostic odds ratio.
        
        Args:
            tp, fn, tn, fp: Confusion matrix values
            
        Returns:
            float: Diagnostic odds ratio
        """
        if fn > 0 and fp > 0:
            dor = (tp * tn) / (fn * fp)
        else:
            dor = float('inf')
        
        return dor
