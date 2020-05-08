dadosBaseline = data.frame(
		c1K = scan('resultados/baseline/1K'),
		c10K = scan('resultados/baseline/10K'),
		c100K = scan('resultados/baseline/100K'),
		c1M = scan('resultados/baseline/1M'),
		c10M = scan('resultados/baseline/10M'),
		c20M = scan('resultados/baseline/20M')
)

dados250M = data.frame(
		c1K = scan('resultados/250M/1K'),
		c10K = scan('resultados/250M/10K'),
		c100K = scan('resultados/250M/100K'),
		c1M = scan('resultados/250M/1M'),
		c10M = scan('resultados/250M/10M'),
		c20M = scan('resultados/250M/20M')
)

dados500M = data.frame(
		c1K = scan('resultados/500M/1K'),
		c10K = scan('resultados/500M/10K'),
		c100K = scan('resultados/500M/100K'),
		c1M = scan('resultados/500M/1M'),
		c10M = scan('resultados/500M/10M'),
		c20M = scan('resultados/500M/20M')
)

dados1G = data.frame(
		c1K = scan('resultados/1G/1K'),
		c10K = scan('resultados/1G/10K'),
		c100K = scan('resultados/1G/100K'),
		c1M = scan('resultados/1G/1M'),
		c10M = scan('resultados/1G/10M'),
		c20M = scan('resultados/1G/20M')
)

#dados5G = data.frame(
#		c1K = scan('resultados/5G/1K'),
#		c10K = scan('resultados/5G/10K'),
#		c100K = scan('resultados/5G/100K'),
#		c1M = scan('resultados/5G/1M'),
#		c10M = scan('resultados/5G/10M'),
#		c20M = scan('resultados/5G/20M')
#)


#dados10G = data.frame(
#		c1K = scan('resultados/10G/1K'),
# 		c10K = scan('resultados/10G/10K'),
#		c100K = scan('resultados/10G/100K'),
#		c1M = scan('resultados/10G/1M'),
#		c10M = scan('resultados/10G/10M'),
#		c20M = scan('resultados/10G/20M')
#)

#dados20G = data.frame(
#		c1K = scan('resultados/20G/1K'),
#		c10K = scan('resultados/20G/10K'),
#		c100K = scan('resultados/20G/100K'),
#		c1M = scan('resultados/20G/1M'),
#		c10M = scan('resultados/20G/10M'),
#		c20M = scan('resultados/20G/20M')
#)

library(lattice)
library(latticeExtra)

cores = c('#3333CC', '#CC0000', '#33FF00', '#990066', '#FFFF33', '#336633')#, '#FF9933')
simbolos = 0:5
rev(simbolos)
ecdfplot(~ c1K + c10K + c100K + c1M + c10M + c20M, dadosBaseline, xlab = "FCT(s)", ylab = "CDF(%)", par.settings = list(fontsize = list(text = 11), superpose.line = list(col = cores), lwd=1.5, lty=1.5), main = list(label = "CDF of FCT - no additional load", cex = 1.5), auto.key = list(text = c('1KB', '10KB', '100KB', '1MB', '10MB', '20MB'), title = "Flow size", space = 'right'))
#legend("left", legend = rev(c('1K', '10K', '100K', '1M', '10M', '20M')), col = rev(cores), lwd = 1)

