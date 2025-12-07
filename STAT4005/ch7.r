# Dickey-Fuller Test
# install.packages("tseries")
# install.packages("quantmod")
library(tseries)
library(quantmod)
x=getSymbols(
	"0005.HK", 
	from="2011-01-01",
	to="2014-12-31", 
	src="yahoo", 
	auto.assign=FALSE
)
y=as.numeric(log(x[!is.na(x[,6]),6]))
adf.test(y, k=0)

# Heteroskedasticity
x=getSymbols(
	"0002.HK", 
	from="2010-01-01",
	to="2016-12-31", 
	src="yahoo", 
	auto.assign=FALSE
)
y=as.numeric(diff(log(x[!is.na(x[,6]),6])))[-1]
par(mfrow=c(3,1))
ts.plot(y) 
acf(y)
acf(y^2)

# Testing for ARCH effect
x=getSymbols(
	"0002.HK", 
	from="2011-01-01", 
	to="2014-12-31", 
	src="yahoo",
	auto.assign=FALSE
)
y=as.numeric(diff(log(x[!is.na(x[,6]),6])))[-1]
y2=y^2
n=length(y)
fit=lm(y2[2:n]~y2[1:(n-1)])
R2=summary(fit)$r.squared
p.value=1-pchisq(n*R2,1)

# Model selection for GARCH model
set.seed(4005)
n=300; burnin=100
x=rep(0,n+burnin)
e=rnorm(n+burnin)
for (i in 3:(n+burnin)) { # Generate ARCH(2) process
	x[i] = e[i]*sqrt(1+0.4*x[i-1]^2+0.5*x[i-2]^2)
}
x=x[-c(1:burnin)]
pacf(x^2)
ans=rep(0,8)
ans[1]=AIC(garch(x,c(1,0)))
ans[2]=AIC(garch(x,c(0,1)))
ans[3]=AIC(garch(x,c(2,0)))
ans[4]=AIC(garch(x,c(0,2)))
ans[5]=AIC(garch(x,c(1,1)))
ans[6]=AIC(garch(x,c(1,2)))
ans[7]=AIC(garch(x,c(2,1)))
ans[8]=AIC(garch(x,c(2,2)))

# Goodness of fit test for GARCH model
x=getSymbols(
	"0002.HK", 
	from="2011-01-01", 
	to="2014-12-31", 
	src="yahoo", 
	auto.assign=FALSE
)
y=as.numeric(diff(log(x[!is.na(x[,6]),6])))[-1]
fit=garch(y,order=c(1,1))
summary(fit)
z=fit$residuals[!is.na(fit$residuals)]
par(mfrow=c(2,2))
acf(y);acf(y^2)
acf(z);acf(z^2)

# Perform Ljung-Box test manually with h = 12
n=length(z)
h=12
r.z=as.numeric(acf(z,h)$acf)
Q=n*(n+2)*sum((r.z[-1]^2)/(n-(1:h)))
Q>qchisq(0.95,h-3)  # FALSE: not reject H0
# Note: Number of parameters estimated in the GARCH(1,1) is 3


# Foreign exchange rates example
ex.s=scan("exchange.dat")
dex=diff(ex.s)
par(mfrow=c(3,2))
ts.plot(ex.s)
acf(ex.s)
ts.plot(dex)
acf(dex)
ts.plot(dex*dex)
acf(dex*dex)

ex.s=scan("exchange.dat")
dex=diff(ex.s)
x1=c(0,dex[1:468])
x2=c(0,0,dex[1:467])
x3=c(0,0,0,dex[1:466])
x4=c(0,0,0,0,dex[1:465])
z1=x1*x1; z2=x2*x2; z3=x3*x3; z4=x4*x4
lm.1=lm(dex*dex~z1+z2+z3+z4)
summary(lm.1)
t=length(dex)*summary(lm.1)$r.squared
1-pchisq(t,4)


library(tseries)
dex.mod=garch(dex,order=c(1,1))
e=dex.mod$residuals
e=e[-1] # (e[1]=NA)
par(mfrow=c(2,2))
ts.plot(e)
acf(e)
acf(e*e)
qqnorm(e)

# U.S. Treasury bill
ttbill=read.table("ustbill.dat")
ttbill=ttbill[,-1]
ttbill=as.vector(t(ttbill))

# Differencing
par(mfrow=c(1,4))
ts.plot(ttbill)
acf(ttbill,40)
dtbill=diff(ttbill)
ts.plot(dtbill)
acf(dtbill,40)

# Residuals plot of ARMA
fit=arima(dtbill,order=c(27,0,0))
res=fit$residuals
par(mfrow=c(1,2))
ts.plot(res^2);acf(res^2)

# Fitting GARCH
ans=matrix(0,6,6)
for (i in 0:5) {
	for (j in 0:5) {
		if ((i==0)&(j==0)) { 
			ans[i+1,j+1]=0
		} else { 
			ans[i+1,j+1]=AIC(garch(res,order=c(i,j)))
		}
	}
}

# Summary of GARCH(1,1)
fit.g=garch(res,order=c(1,1))
summary(fit.g)
acf(fit.g$res[-c(1:9)]^2) # The first 9 NA entries should be removed.
