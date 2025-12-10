==**Lecture 7: Beyond Formulas**==

<font color="navy">**Notation**</font>
• $N$: Population size
• $n$: Sample size
• $\tau$: Population total
• $\mu$: Population mean
• $k$: Sampling interval (in systematic context) or scale length (in Likert context)

<font color="navy">**调查误差主要分为两类：非观测误差 (Errors of Non-observation) 和 观测误差 (Errors of Observation)。**</font>
<font color="navy">**1.1 Errors of Non-observation**</font>
这类误差源于我们未能观测到总体中的某些部分。
• Sampling Error: The difference between our estimate and the true parameter value due to the sampling. (Can be reduced by appropriate sample design and increasing sample size $n$).
• Error of Coverage: Occurs when the sampling frame does not contain every sampling unit in the population (e.g., outdated lists, unlisted numbers).
• Non-response: The most serious non-observation error. It happens in three ways:
<font color="navy">1.</font> Inability to contact: The sample element cannot be reached (e.g., not at home).
<font color="navy">2.</font> Inability to answer: The respondent lacks the knowledge or opinion to answer.
<font color="navy">3.</font> Refusal to answer: The respondent deliberately declines to participate.
<font color="navy">**1.2 Errors of Observation**</font>
这类误差发生在已经联系上受访者并进行观测的过程中，由以下四个因素引起：
• Error due to the interviewer: Interviewers may influence responses through intonation, emphasis, or by creating a sense of confrontation.
• Error due to the respondent:
<font color="navy">a)</font> Recall bias: Respondent recalls information incorrectly.
<font color="navy">b)</font> Prestige bias: Respondent exaggerates answers to look good.
<font color="navy">c)</font> Intentional deception: Respondent deliberately lies.
<font color="navy">d)</font> Incorrect measurement: Respondent misunderstands the question or units.
• Error due to the measurement instrument: Concepts defined ambiguously (e.g., "glass of water", "unemployed").
• Error due to the method of data collection:
<font color="navy">i)</font> Personal interviews: Good response rate but expensive; risk of interviewer bias.
<font color="navy">ii)</font> Telephone interviews: Cheaper but harder to get a complete frame; must be shorter.
<font color="navy">iii)</font> Self-administered questionnaires: Cheapest but high non-response rate and potential bias.
<font color="navy">iv)</font> Direct observation: Less bias but prone to human error.

<font color="navy">**2. Reducing Errors**</font>
为了减少非抽样误差，我们可以采取以下措施：
• Callbacks: Re-attempting to contact sampling elements at different times to reduce non-response.
• Rewards / Incentives: Offering benefits (money, products) to encourage participation. Note: Rewards should be offered after selection to avoid selection bias.
• Interviewer training: Training interviewers to remain neutral and encourage honest responses.
• Data checks: Performing logic checks (e.g., proportions between 0 and 1) after data collection.

<font color="navy">**3. Question Design**</font>
问卷设计是减少非抽样误差的关键。设计时需注意以下原则：
<font color="navy">3.1 Ordering Effects</font>
• It is usually better to ask general questions first, then follow with specific questions.
• Previous questions can change the frame of mind of a respondent (priming effect).
<font color="navy">3.2 Types of Questions</font>
• Closed questions: Have fixed choices or single numerical answers. Easier to analyze but restrictive.
• Open questions: Allow free-form answers. Yield nuanced data but hard to analyze. (Often used in pre-tests to design closed questions).
<font color="navy">3.3 Handling Uncertainty</font>
• "Don't know" options: Excluding these forces an opinion; including them may lead to laziness. Use screening questions to filter knowledgeable respondents.
• Middle-ground options: A neutral midpoint prevents forcing a direction but acts as an "easy out".
<font color="navy">3.4 Wording Pitfalls to Avoid</font>
• Leading questions: Questions phrased to favor a specific answer (e.g., "Do you agree that...").
• Unbalanced questions: Offering only one side of an argument. (Should use "Do you favor or oppose...").
• Argumentative tone: Using strong words like "forbid" vs "not allow".
• Double-barrelled questions: Asking about two concepts in one question (e.g., "Bill Clinton AND the loan to Mexico").
• Ambiguity: Unclear definitions (e.g., "How much water do you drink?").
<font color="navy">3.5 Memory Errors</font>
• Telescoping: Recent events seem more distant, and memorable distant events seem more recent.
• Solution: Relate questions to specific memorable events (anchoring) or use direct observation.

<font color="navy">**4. Likert Scales**</font>
Likert 量表用于测量态度或意见：
• Likert items: Statements where respondents choose a level of agreement (e.g., "Strongly Agree" to "Strongly Disagree").
• Likert scale: The sum or average of scores from multiple Likert items representing an overall attitude.
• Scale points: Usually 5 or 7 points. Odd numbers are preferred to provide a neutral midpoint (e.g., "Undecided").

<font color="navy">**5. Interpreting Results**</font>
在解释调查结果时，必须注意因果关系的推断风险：
• Confounding variables: Factors not considered by researchers that affect both the suspected cause and the effect.
• Simpson's Paradox: A trend that appears in groups of data can disappear or reverse when the groups are aggregated. (Example: Berkeley Sex Bias study, where department choice was the confounding variable).
• Correlation does not imply causation.

<font color="navy">**6. Planning a Survey (11-Point Plan)**</font>
规划调查时应遵循以下步骤：
<font color="navy">1.</font> Statement of objectives: Define clear, simple goals.
<font color="navy">2.</font> Target population: Define precisely.
<font color="navy">3.</font> The frame: Choose frames covering the population (multiple frames if needed).
<font color="navy">4.</font> Sample design: Determine method and sample size $n$.
<font color="navy">5.</font> Method of measurement: Interview vs. Questionnaire vs. Observation.
<font color="navy">6.</font> Measurement instrument: Design the questionnaire.
<font color="navy">7.</font> Selection and training of fieldworkers.
<font color="navy">8.</font> The pretest: Test design and estimate parameters.
<font color="navy">9.</font> Organization of fieldwork: Logistics.
<font color="navy">10.</font> Organization of data management: Handling large data.
<font color="navy">11.</font> Data analysis: Plan analysis methods beforehand.

==**Lecture 8: Applied Problems**==

<font color="navy">**Notation**</font>
• $N$: Population size
• $n$: Sample size
• $L$: Number of strata
• $N_i$: Population size of stratum $i$ (or subpopulation $i$)
• $n_i$: Sample size observed in stratum $i$ (random in post-stratification)
• $\overline{Y}_{pst}$: Post-stratified estimator of the mean
• $\hat{\phi}$: Sample proportion of "Yes" answers in Random Response Model
• $p$: Proportion of population in Group A (sensitive group)
• $p_S$: Probability of answering the sensitive question
• $p_{Yes|T}$: Probability of answering "Yes" to the trivial question
• $\hat{\sigma}_i^2$: Sample variance of stratum/subpopulation $i$ (denominator $n_i-1$)
• $\tau_1$: Subpopulation total
• $U_i$: Auxiliary variable for subpopulation ($Y_i$ if in subpop, 0 otherwise)

<font color="navy">**1. Random Response Model**</font>
Used to estimate proportion $p$ of a sensitive group (Group A) when respondents may not answer truthfully. Uses a randomization device (e.g., coin).  一般用于问你是Group A还是Group B这样的二分类问题。
• Setup:
<font color="navy">1.</font> Sensitive Question: "Are you in Group A?"
<font color="navy">2.</font> Trivial Question: "Is the last digit of your phone number even?" (Known probability $p_{Yes|T}$).
<font color="navy">3.</font> Randomization device: Answer sensitive question with probability $p_S$, trivial with $1-p_S$.
• Estimator:
By Law of Total Probability: $\phi = p\cdot p_S + p_{Yes|T}(1-p_S)$.
The estimator for $p$ is:$\hat{p} = \left[ \hat{\phi} - p_{Yes|T}(1-p_S) \right] / p_S$
• Variance:$$\widehat{Var}(\hat{p}) = {\widehat{Var}(\hat{\phi})}\big /{p_S^2} = \frac{1}{p_S^2}\left(1-\frac{n}{N}\right)\frac{1}{n-1}\hat{\phi}(1-\hat{\phi})$$
<font color="navy">Note</font>: The factor $\frac{1}{p_S^2}$ represents the variance penalty for using the random response model. Variance is larger than direct questioning.

<font color="navy">**2. Post-Stratification**</font>
Used when strata cannot be determined *before* sampling (e.g., gender in a phone survey), but stratum weights $N_i/N$ are known. The sample sizes $n_i$ are random variables.
• Estimator:$$\overline{Y}_{pst} = \sum_{i=1}^{L} \frac{N_i}{N}\overline{Y}_i$$ , where $\overline{Y}_i$ is the sample mean of stratum $i$.
• Variance Estimator:
$$
\widehat{Var}(\overline{Y}_{pst}) = \sum_{i=1}^{L}\frac{N-n}{nN}\frac{N_i}{N}\hat{\sigma}_i^2 + \sum_{i=1}^{L}\frac{1}{n^2}\frac{N-n}{N-1}\left(1-\frac{N_i}{N}\right)\hat{\sigma}_i^2
$$
<font color="navy">Interpretation</font>:
• First term: Equivalent to stratified sampling with proportional allocation.
• Second term: The increase in variance due to the randomness of $n_i$. When n is large, the increase is small.
• Condition: Only use post-stratification when $n$ and all $n_i$ are reasonably large.

<font color="navy">**3. Adjusting for Non-response**</font>
Non-response introduces bias if non-respondents differ from respondents.
High non-response rate $\Rightarrow$ sample not properly reflect the groupings in  the population $\Rightarrow$ some stratum is over-represented
<font color="red">3.1 Post-stratification Adjustment</font>
• Use when population stratum proportions $N_i/N$ are known.
• Treat respondents as the sample and adjust weights to match population $N_i/N$.
• Use $\overline{Y}_{pst}$ formulas.
• Effect: 1. Correct the estimate 2. standard deviation has reduced, because of the small variance within groups.
<font color="red">3.2 Weight-class Adjustment</font>
• Use when population stratum proportions $N_i/N$ are unknown.
• Estimate stratum sizes $\hat{N}_i$ from the initial sample (including non-respondents).  $$\hat{N}_i = N \cdot {n_{i, \text{total}}}/{n_{\text{total}}}$$  • Estimator: $\overline{y}_{wc} = \sum \frac{\hat{N}_i}{N}\overline{y}_i$.
• Effect: 1. This estimate is biased because of the estimation of the stratum sizes. 2. Variance is even smaller. 

<font color="navy">**4. Subpopulations (Domains)**</font>
Estimating parameters for a specific subpopulation (size $N_1$) where membership is not known prior to sampling.
<font color="navy">**4.1 Estimating Subpopulation Mean** $\mu_1 = \frac {1} {N_1} \sum_{j=1} ^ {N_1} Y_{1j}$</font>
• Estimator: $\hat{\mu}_1 = \overline{Y}_1 = \frac{1}{n_1}\sum_{i=1}^{n_1} Y_{1i}$ (This is technically a ratio estimator because $n_1$ is random).
• Variance Estimator:$\widehat{Var}(\overline{Y}_1) = \frac{N^2}{N_1^2}\left(1-\frac{n}{N}\right)\frac{1}{n}\frac{n_1-1}{n-1}\hat{\sigma}_1^2$
If $N_1/N$ is unknown, approximate using $n_1/n$:$\widehat{Var}(\overline{Y}_1) = \left(1-\frac{n}{N}\right)(\frac{n}{n-1})(\frac{n_1-1}{n_1})\frac{\hat{\sigma}_1^2}{n_1}$ $ \approx \left(1-\frac{n}{N}\right)\frac{\hat{\sigma}_1^2}{n_1}$ when $n, n_1$ are large
<font color="navy">**4.2 Estimating Subpopulation Total $\tau_1$**</font>
•<font color=red> Case A</font>: $N_1$ is Known$$\hat{\tau}_1 = N_1 \overline{Y}_1$$
$$\widehat{Var}(\hat{\tau}_1) = N_1^2 \widehat{Var}(\overline{Y}_1) \approx N_1^2 \left(1-\frac{n}{N}\right)\frac{\hat{\sigma}_1^2}{n_1}$$
This has lower variance (preferred).
• <font color=red> Case B</font>: $N_1$ is Unknown
Define variable $U_i = Y_i$ if element $i$ is in subpopulation, $0$ otherwise.
$$\hat{\tau}_1 = \frac{N}{n}\sum_{i=1}^{n} U_i = N\overline{U}$$
$$\widehat{Var}(\hat{\tau}_1) = N^2\left(1-\frac{n}{N}\right)\frac{\hat{\sigma}_u^2}{n}$$
• Calculation of $\hat{\sigma}_u^2$:
Sample variance of $U$ (including the $n-n_1$ zeros). $$\hat{\sigma}_u^2 = \frac{1}{n-1}\left(\sum_{i=1}^{n} U_i^2 - n(\overline{U})^2\right)$$, where $\sum U_i^2 = \sum_{j=1}^{n_1} y_{1j}^2$.
$y_{1j}$ 就是你抽到的那 $n_1$ 个“有效样本”（子总体成员）的具体数值。
<font color="navy">Note</font>: This estimator has higher variance because the zeros in $U$ inflate the variance ($\hat{\sigma}_u^2 > \hat{\sigma}_1^2$). 