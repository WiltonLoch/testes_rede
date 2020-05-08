dados1K = data.frame(
		baseline = scan('resultados/baseline/1K'),
		c250m = scan('resultados/250M/1K'),
		c500m = scan('resultados/500M/1K'),
		c1G = scan('resultados/1G/1K'),
		c5G = scan('resultados/5G/1K'),
		c10G = scan('resultados/10G/1K'),
		c20G = scan('resultados/20G/1K')
)

dados10K = data.frame(
		baseline = scan('resultados/baseline/10K'),
		c250m = scan('resultados/250M/10K'),
		c500m = scan('resultados/500M/10K'),
		c1G = scan('resultados/1G/10K'),
		c5G = scan('resultados/5G/10K'),
		c10G = scan('resultados/10G/10K'),
		c20G = scan('resultados/20G/10K')
)

dados100K = data.frame(
		baseline = scan('resultados/baseline/100K'),
		c250m = scan('resultados/250M/100K'),
		c500m = scan('resultados/500M/100K'),
		c1G = scan('resultados/1G/100K'),
		c5G = scan('resultados/5G/100K'),
		c10G = scan('resultados/10G/100K'),
		c20G = scan('resultados/20G/100K')
)

dados1M = data.frame(
		baseline = scan('resultados/baseline/1M'),
		c250m = scan('resultados/250M/1M'),
		c500m = scan('resultados/500M/1M'),
		c1G = scan('resultados/1G/1M'),
		c5G = scan('resultados/5G/1M'),
		c10G = scan('resultados/10G/1M'),
		c20G = scan('resultados/20G/1M')
)

dados10M = data.frame(
		baseline = scan('resultados/baseline/10M'),
		c250m = scan('resultados/250M/10M'),
		c500m = scan('resultados/500M/10M'),
		c1G = scan('resultados/1G/10M'),
		c5G = scan('resultados/5G/10M'),
		c10G = scan('resultados/10G/10M'),
		c20G = scan('resultados/20G/10M')
)

dados20M = data.frame(
		baseline = scan('resultados/baseline/20M'),
		c250m = scan('resultados/baseline/20M'),
		c500m = scan('resultados/500M/20M'),
		c1G = scan('resultados/1G/20M'),
		c5G = scan('resultados/5G/20M'),
		c10G = scan('resultados/10G/20M'),
		c20G = scan('resultados/20G/20M')
)


resumo_dados = data.frame(
	t1K = c(
		median(dados1K$baseline),
		median(dados1K$c250m),
		median(dados1K$c500m),
		median(dados1K$c1G),
		median(dados1K$c5G),
		median(dados1K$c10G),
		median(dados1K$c20G)
		),
	t10K = c(
		median(dados10K$baseline),
		median(dados10K$c250m),
		median(dados10K$c500m),
		median(dados10K$c1G),
		median(dados10K$c5G),
		median(dados10K$c10G),
		median(dados10K$c20G)
		),
	t100K = c(
		median(dados100K$baseline),
		median(dados100K$c250m),
		median(dados100K$c500m),
		median(dados100K$c1G),
		median(dados100K$c5G),
		median(dados100K$c10G),
		median(dados100K$c20G)
		),
	t1M = c(
		median(dados1M$baseline),
		median(dados1M$c250m),
		median(dados1M$c500m),
		median(dados1M$c1G),
		median(dados1M$c5G),
		median(dados1M$c10G),
		median(dados1M$c20G)
		),
	t10M = c(
		median(dados10M$baseline),
		median(dados10M$c250m),
		median(dados10M$c500m),
		median(dados10M$c1G),
		median(dados10M$c5G),
		median(dados10M$c10G),
		median(dados10M$c20G)
		),
	t20M = c(
		median(dados20M$baseline),
		median(dados20M$c250m),
		median(dados20M$c500m),
		median(dados20M$c1G),
		median(dados20M$c5G),
		median(dados20M$c10G),
		median(dados20M$c20G)
		)
	)

cores = c('#3333CC', '#CC0000', '#33FF00', '#990066', '#FFFF33', '#336633')#, '#FF9933')
simbolos = 0:6
rev(simbolos)
matplot(resumo_dados, type = "b", xlab = "Tráfego adicional no gargalo(bps)", ylab = "FCT(s)", ylim = c(0,12), col = cores, pch = simbolos, axes = F )
axis(side = 2)
axis(side = 1, at=1:nrow(resumo_dados), labels = c('Sem carga', '250M', '500M', '1G', '5G', '10G', '20G'))
legend("left", legend = rev(c('1K', '10K', '100K', '1M', '10M', '20M')), col = rev(cores), pch = rev(simbolos), lwd = 1)
