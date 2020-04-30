dados = data.frame(
	t1K = c(
		mean(scan('resultados/baseline/1K')),
		mean(scan('resultados/250M/1K')),
		mean(scan('resultados/500M/1K')),
		mean(scan('resultados/1G/1K')),
		mean(scan('resultados/5G/1K')),
		mean(scan('resultados/10G/1K')),
		mean(scan('resultados/20G/1K'))
		),
	t10K = c(
		mean(scan('resultados/baseline/10K')),
		mean(scan('resultados/250M/10K')),
		mean(scan('resultados/500M/10K')),
		mean(scan('resultados/1G/10K')),
		mean(scan('resultados/5G/10K')),
		mean(scan('resultados/10G/10K')),
		mean(scan('resultados/20G/10K'))
		),
	t100K = c(
		mean(scan('resultados/baseline/100K')),
		mean(scan('resultados/250M/100K')),
		mean(scan('resultados/500M/100K')),
		mean(scan('resultados/1G/100K')),
		mean(scan('resultados/5G/100K')),
		mean(scan('resultados/10G/100K')),
		mean(scan('resultados/20G/100K'))
		),
	t1M = c(
		mean(scan('resultados/baseline/1M')),
		mean(scan('resultados/250M/1M')),
		mean(scan('resultados/500M/1M')),
		mean(scan('resultados/1G/1M')),
		mean(scan('resultados/5G/1M')),
		mean(scan('resultados/10G/1M')),
		mean(scan('resultados/20G/1M'))
		),
	t10M = c(
		mean(scan('resultados/baseline/10M')),
		mean(scan('resultados/250M/10M')),
		mean(scan('resultados/500M/10M')),
		mean(scan('resultados/1G/10M')),
		mean(scan('resultados/5G/10M')),
		mean(scan('resultados/10G/10M')),
		mean(scan('resultados/20G/10M'))
		),
	t20M = c(
		mean(scan('resultados/baseline/20M')),
		mean(scan('resultados/250M/20M')),
		mean(scan('resultados/500M/20M')),
		mean(scan('resultados/1G/20M')),
		mean(scan('resultados/5G/20M')),
		mean(scan('resultados/10G/20M')),
		mean(scan('resultados/20G/20M'))
		)
	)

cores = c('#3333CC', '#CC0000', '#33FF00', '#990066', '#FFFF33', '#336633')#, '#FF9933')
simbolos = 0:5
rev(simbolos)
matplot(dados, type = "b", xlab = "Tráfego adicional no gargalo(bps)", ylab = "FCT(s)", ylim = c(0,10), col = cores, pch = simbolos, axes = F )
axis(side = 2)
axis(side = 1, at=1:nrow(dados), labels = c('Sem carga', '250M', '500M', '1G', '5G', '10G', '20G'))
legend("left", legend = rev(c('1K', '10K', '100K', '1M', '10M', '20M')), col = rev(cores), pch = rev(simbolos), lwd = 1)
