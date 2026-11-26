SELECT perturbation, cell_type, COUNT(*) AS n_samples, AVG(dose) AS mean_dose
FROM perturbation_samples
GROUP BY 1, 2
ORDER BY n_samples DESC;

SELECT batch, COUNT(*) AS n_samples, COUNT(DISTINCT perturbation) AS perturbations
FROM perturbation_samples
GROUP BY 1
ORDER BY 1;
