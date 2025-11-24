#SID: 1155211130
#Name: DaiDasen
Y <- c(
  1.33, -0.56, -1.31, -0.37, 0.05,
  0.46,  2.00, -0.19, -0.25, 1.07,
  -0.17,  1.14,  0.63, -0.75, 0.15,
  0.71,  0.45, -0.14, 0.57,  1.43
)

n  <- length(Y)
yt <- ts(Y)

## (1)===============================

## Plot 1: time series
plot.ts(yt,
        main = "Time Series Plot of Y_t",
        ylab = "Y_t", xlab = "t")

## Plot 2: ACF
acf(yt,
    main = "Sample ACF of Y_t")

## Plot 3: PACF
pacf(yt,
     main = "Sample PACF of Y_t")



## (2)===============================

acf_lag1 <- acf(yt, plot = FALSE, lag.max = 1)
r1 <- as.numeric(acf_lag1$acf[2])
theta_from_r1 <- function(r1) {
  if (abs(r1) > 0.5) {
    warning("|r1| > 0.5")
    return(NA)
  }
  f <- function(theta) theta / (1 + theta^2) - r1
  uniroot(f, interval = c(-0.99, 0.99))$root
}

theta_mom <- theta_from_r1(r1)

Y_centered  <- Y - mean(Y)
gamma0_hat  <- sum(Y_centered^2) / n
sigma2_mom  <- gamma0_hat / (1 + theta_mom^2)

cat("theta_hat (moment) =", theta_mom, "\n")
cat("sigma2_hat (moment) =", sigma2_mom, "\n")



## (3)===============================

p  <- 2
n  <- length(Y)
n0 <- n - p

Y_vec <- Y[(p + 1):n]
X_mat <- cbind(Y_lag1 = Y[2:(n - 1)],
               Y_lag2 = Y[1:(n - 2)])

XtX     <- t(X_mat) %*% X_mat
XtY     <- t(X_mat) %*% Y_vec
phi_hat <- solve(XtX, XtY)

phi1_ls <- phi_hat[1]
phi2_ls <- phi_hat[2]

resid     <- Y_vec - X_mat %*% phi_hat
sigma2_ls <- as.numeric(t(resid) %*% resid) / (n0 - p)

cat("phi1_hat =", phi1_ls, "\n")
cat("phi2_hat =", phi2_ls, "\n")
cat("sigma2_hat =", sigma2_ls, "\n")

Yc <- Y - mean(Y)
Ck <- function(k) sum(Yc[(k + 1):n] * Yc[1:(n - k)]) / n
C0 <- Ck(0); C1 <- Ck(1)

Gamma_hat   <- matrix(c(C0, C1, C1, C0), nrow = 2, byrow = TRUE)
Var_phi_hat <- (sigma2_ls / n) * solve(Gamma_hat)
se_phi      <- sqrt(diag(Var_phi_hat))

z <- qnorm(0.975)
CI_phi1 <- c(phi1_ls - z * se_phi[1], phi1_ls + z * se_phi[1])
CI_phi2 <- c(phi2_ls - z * se_phi[2], phi2_ls + z * se_phi[2])

cat("95% CI for phi1: [", CI_phi1[1], ", ", CI_phi1[2], "]\n", sep = "")
cat("95% CI for phi2: [", CI_phi2[1], ", ", CI_phi2[2], "]\n", sep = "")


## (4)===============================

fit_ar2_yw <- ar(yt,
                 aic       = FALSE,
                 order.max = 2,
                 method    = "yw")

phi_yw    <- fit_ar2_yw$ar        # (phi1, phi2)
sigma2_yw <- fit_ar2_yw$var.pred  

cat("phi1_hat (YW) =", phi_yw[1], "\n")
cat("phi2_hat (YW) =", phi_yw[2], "\n")
cat("sigma2_hat (YW) =", sigma2_yw, "\n")


## (5)===============================

S_arma11 <- function(beta){
  phi   <- beta[1]
  theta <- beta[2]
  Z <- numeric(n)
  Z[1] <- Y[1]              
  for(t in 2:n){
    Z[t] <- Y[t] - phi*Y[t-1] - theta*Z[t-1]
  }
  sum(Z^2)                    
}

CLS_fit   <- optim(c(0.1, 0.1), S_arma11)
phi_cls   <- CLS_fit$par[1]
theta_cls <- CLS_fit$par[2]
sigma2_cls <- CLS_fit$value / (n)   # sigma^2_hat = S*(phihat,thetahat)/(n-1)

cat("phi_hat (CLS)   =", phi_cls,   "\n")
cat("theta_hat (CLS) =", theta_cls, "\n")
cat("sigma2_hat (CLS)=", sigma2_cls,"\n")


## (6)===============================

fit_arma11_ml <- arima(yt,
                       order        = c(1, 0, 1),
                       include.mean = FALSE,
                       method       = "ML")

coef_ml   <- coef(fit_arma11_ml)
phi_ml    <- coef_ml["ar1"]
theta_ml  <- coef_ml["ma1"]
sigma2_ml <- fit_arma11_ml$sigma2
loglik_ml <- as.numeric(logLik(fit_arma11_ml))

cat("phi_hat (ML) =", phi_ml, "\n")
cat("theta_hat (ML) =", theta_ml, "\n")
cat("sigma2_hat (ML) =", sigma2_ml, "\n")
cat("maximized log-likelihood =", loglik_ml, "\n")

## (7)===============================
FPE_ar <- function(x, p){
  n   <- length(x)
  fit <- arima(x, order = c(p,0,0), include.mean = FALSE, method = "ML")
  sig2 <- fit$sigma2
  sig2 * (n + p) / (n - p)
}

p_seq    <- 1:5
fpe_vals <- sapply(p_seq, function(p) FPE_ar(Y, p))
cbind(p = p_seq, FPE = fpe_vals)
best_p <- which.min(fpe_vals)
best_p



## (8)===============================
AICC_ma <- function(x, q){
  n   <- length(x)
  fit <- arima(x, order = c(0,0,q), include.mean = FALSE, method = "ML")
  loglik <- as.numeric(logLik(fit))
  k <- q + 1
  -2 * loglik + 2 * k * n / (n - k - 1)
}

q_seq      <- 1:5
aicc_vals  <- sapply(q_seq, function(q) AICC_ma(Y, q))
cbind(q = q_seq, AICC = aicc_vals)
best_q <- which.min(aicc_vals)
best_q



## (9)===============================
fit_ma1 <- arima(Y, order = c(0,0,1), include.mean = FALSE, method = "ML")

resid_ma1 <- residuals(fit_ma1)
resid_ma1

r <- as.numeric(acf(resid_ma1, lag.max = 10, plot = FALSE)$acf)[-1]  # r_Z(1)...r_Z(10)
Q10 <- n * (n + 2) * sum(r[1:10]^2 / (n - (1:10)))
Q10

Box.test(resid_ma1, lag = 10, type = "Ljung-Box", fitdf = 1)

