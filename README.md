
# CCF Searcher

A paper tool that searches papers in CCF.

## Features

* Make your search results more precise

## How to Work

Crawling data from [dblp.com](https://dblp.uni-trier.de/), then processing these data with `pandas`.

## Usage

### dblp_crawler.py

It will take a long time to crawl the data.

```shell
python3 dblp_crawler.py
```

### ccf_searcher_example.ipynb

```shell
jupyter lab ccf_searcher_example.ipynb
```

Using more accurate searcher.

```python
# ------------- Paper Quality -------------
df2 = df[(df['year'] >= 2018) | (df["year"] == -1)]
df2 = df2[(df2['ccf_rank'].str.contains('CCF-A|CCF-B', case=False))]
# ------------- Field         -------------
df2 = df2[(df2['title'].str.contains('reinforcement|multi-armed', case=False))]
# ------------- Direction     -------------
df2 = df2[(df2['title'].str.contains('adversarial', case=False))]
# ------------- Conference / Journal   -------------
df2 = df2[(df2['ccf_name'].str.contains('USENIX|AAAI', case=False))]

df2 = df2.sort_values(['ccf_rank', 'year', 'abbreviation'], ascending=[True, False, False])
df3 = df2[["ccf_rank", "ccf_name", "year", "title", "authors"]].copy() # Show
df3.authors = df3['authors'].str[:32]
print('Count: ', len(df3))
display(df3.head(100).style)
display(pd.DataFrame(df2.groupby(['ccf_rank', 'ccf_name']).size().sort_values(ascending=False)).style)
```

**Output**

---

#### CCF-A (7)
##### Usenix Security Symposium (2)
1. 2021, [Adversarial Policy Training against Deep Reinforcement Learning](https://www.usenix.org/conference/usenixsecurity21/presentation/wu-xian)
2. 2020, [EcoFuzz: Adaptive Energy-Saving Greybox Fuzzing as a Variant of the Adversarial Multi-Armed Bandit](https://www.usenix.org/conference/usenixsecurity20/presentation/yue)
##### AAAI Conference on Artificial Intelligence (5)
1. 2021, [Resilient Multi-Agent Reinforcement Learning with Adversarial Value Decomposition](https://ojs.aaai.org/index.php/AAAI/article/view/17348)
2. 2021, [Reinforcement Based Learning on Classification Task Yields Better Generalization and Adversarial Accuracy (Student Abstract)](https://ojs.aaai.org/index.php/AAAI/article/view/17893)
3. 2020, [Finding Needles in a Moving Haystack: Prioritizing Alerts with Adversarial Reinforcement Learning](https://ojs.aaai.org/index.php/AAAI/article/view/5442)
4. 2020, [Stealthy and Efficient Adversarial Attacks against Deep Reinforcement Learning](https://ojs.aaai.org/index.php/AAAI/article/view/6047)
5. 2018, [OptionGAN: Learning Joint Reward-Policy Options Using Generative Adversarial Inverse Reinforcement Learning](https://dblp.uni-trier.de/rec/conf/aaai/0002CBMPP18.html?view=bibtex)

### Rank Server

Query CCF-rank of paper in website quickly.

Preview website: [ccf-rank.eonew.cn](http://ccf-rank.eonew.cn)

### paper_to_ccf_rank_example.ipynb

Same as `Rank Server`.

### abstract_crawler.py

Crawl abstract according to the file `abstract_crawler_input.json`.

```shell
python3 abstract_crawler.py
```

### abstract_searcher_example.ipynb

```shell
jupyter lab abstract_searcher_example.ipynb
```

Using more accurate searcher.

```python
# ------------- Paper Quality -------------
df2 = df[(df['year'] >= 2018) | (df["year"] == -1)]
df2 = df2[(df2['ccf_rank'].str.contains('CCF-A|CCF-B', case=False))]
# ------------- Field         -------------
df2 = df2[(df2['title'].str.contains('reinforcement|multi-armed', case=False))]
# ------------- Direction     -------------
df2 = df2[(df2['title'].str.contains('adversarial', case=False))]
# ------------- Conference / Journal   -------------
df2 = df2[(df2['ccf_name'].str.contains('USENIX|AAAI', case=False))]

df2 = df2.sort_values(['ccf_rank', 'year', 'abbreviation'], ascending=[True, False, False])
df3 = df2[["ccf_rank", "ccf_name", "year", "title", "authors"]].copy() # Show
df3.authors = df3['authors'].str[:32]
print('Count: ', len(df3))
display(df3.head(100).style)
display(pd.DataFrame(df2.groupby(['ccf_rank', 'ccf_name']).size().sort_values(ascending=False)).style)
```

**Output**

---

#### ACM Conference on Computer and Communications Security (3)

1. **[Structural Attack against Graph Based Android Malware Detection](https://doi.org/10.1145/3460120.3485387)**

    **Authors**: Kaifa Zhao, Hao Zhou, Yulin Zhu, Xian Zhan, Kai Zhou, Jianfeng Li, Le Yu, Wei Yuan, Xiapu Luo

    **Year**: 2021

    **Abstract**:

    Malware detection techniques achieve great success with deeper insight into the semantics of malware. Among existing detection techniques, function call graph (FCG) based methods achieve promising performance due to their prominent representations of malware's functionalities. Meanwhile, recent adversarial attacks not only perturb feature vectors to deceive classifiers (i.e., feature-space attacks) but also investigate how to generate real evasive malware (i.e., problem-space attacks). However, existing problem-space attacks are limited due to their inconsistent transformations between feature space and problem space.

    In this paper, we propose the first structural attack against graph-based Android malware detection techniques, which addresses the inverse-transformation problem [1] between feature-space attacks and problem-space attacks. We design a Heuristic optimization model integrated with Reinforcement learning framework to optimize our structural ATtack (HRAT). HRAT includes four types of graph modifications (i.e., inserting and deleting nodes, adding edges and rewiring) that correspond to four manipulations on apps (i.e., inserting and deleting methods, adding call relation, rewiring). Through extensive experiments on over 30k Android apps, HRAT demonstrates outstanding attack performance on both feature space (over 90% attack success rate) and problem space (up to 100% attack success rate in most cases). Besides, the experiment results show that combing multiple attack behaviors strategically makes the attack more effective and efficient.

2. **[A Tale of Evil Twins: Adversarial Inputs versus Poisoned Models](https://doi.org/10.1145/3372297.3417253)**

    **Authors**: Ren Pang, Hua Shen, Xinyang Zhang, Shouling Ji, Yevgeniy Vorobeychik, Xiapu Luo, Alex X. Liu, Ting Wang

    **Year**: 2020

    **Abstract**:

    Despite their tremendous success in a range of domains, deep learning systems are inherently susceptible to two types of manipulations: adversarial inputs -- maliciously crafted samples that deceive target deep neural network (DNN) models, and poisoned models -- adversely forged DNNs that misbehave on pre-defined inputs. While prior work has intensively studied the two attack vectors in parallel, there is still a lack of understanding about their fundamental connections: what are the dynamic interactions between the two attack vectors? what are the implications of such interactions for optimizing existing attacks? what are the potential countermeasures against the enhanced attacks? Answering these key questions is crucial for assessing and mitigating the holistic vulnerabilities of DNNs deployed in realistic settings.

    Here we take a solid step towards this goal by conducting the first systematic study of the two attack vectors within a unified framework. Specifically, (i) we develop a new attack model that jointly optimizes adversarial inputs and poisoned models; (ii) with both analytical and empirical evidence, we reveal that there exist intriguing "mutual reinforcement" effects between the two attack vectors -- leveraging one vector significantly amplifies the effectiveness of the other; (iii) we demonstrate that such effects enable a large design spectrum for the adversary to enhance the existing attacks that exploit both vectors (e.g., backdoor attacks), such as maximizing the attack evasiveness with respect to various detection methods; (iv) finally, we discuss potential countermeasures against such optimized attacks and their technical challenges, pointing to several promising research directions.

3. **[Seeing isn't Believing: Towards More Robust Adversarial Attack Against Real World Object Detectors](https://doi.org/10.1145/3319535.3354259)**

    **Authors**: Yue Zhao, Hong Zhu, Ruigang Liang, Qintao Shen, Shengzhi Zhang, Kai Chen

    **Year**: 2019

    **Abstract**:

    Recently Adversarial Examples (AEs) that deceive deep learning models have been a topic of intense research interest. Compared with the AEs in the digital space, the physical adversarial attack is considered as a more severe threat to the applications like face recognition in authentication, objection detection in autonomous driving cars, etc. In particular, deceiving the object detectors practically, is more challenging since the relative position between the object and the detector may keep changing. Existing works attacking object detectors are still very limited in various scenarios, e.g., varying distance and angles, etc. In this paper, we presented systematic solutions to build robust and practical AEs against real world object detectors. Particularly, for Hiding Attack (HA), we proposed thefeature-interference reinforcement (FIR) method and theenhanced realistic constraints generation (ERG) to enhance robustness, and for Appearing Attack (AA), we proposed thenested-AE, which combines two AEs together to attack object detectors in both long and short distance. We also designed diverse styles of AEs to make AA more surreptitious. Evaluation results show that our AEs can attack the state-of-the-art real-time object detectors (i.e., YOLO V3 and faster-RCNN) at the success rate up to 92.4% with varying distance from 1m to 25m and angles from -60º to 60º. Our AEs are also demonstrated to be highly transferable, capable of attacking another three state-of-the-art black-box models with high success rate.

#### Usenix Security Symposium (3)

1. **[Adversarial Policy Training against Deep Reinforcement Learning](https://www.usenix.org/conference/usenixsecurity21/presentation/wu-xian)**

    **Authors**: Xian Wu, Wenbo Guo, Hua Wei, Xinyu Xing

    **Year**: 2021

    **Abstract**:

    Reinforcement learning is a set of goal-oriented learning algorithms, through which an agent could learn to behave in an environment, by performing certain actions and observing the reward which it gets from those actions. Integrated with deep neural networks, it becomes deep reinforcement learning, a new paradigm of learning methods. Recently, deep reinforcement learning demonstrates great potential in many applications such as playing video games, mastering GO competition, and even performing autonomous pilot. However, coming together with these great successes is adversarial attacks, in which an adversary could force a well-trained agent to behave abnormally by tampering the input to the agent's policy network or training an adversarial agent to exploit the weakness of the victim. 

    In this work, we show existing adversarial attacks against reinforcement learning either work in an impractical setting or perform less effectively when being launched in a two-agent zero-sum game. Motivated by this, we propose a new method to train adversarial agents. Technically speaking, our approach extends the Proximal Policy Optimization (PPO) algorithm and then utilizes an explainable AI technique to guide an attacker to train an adversarial agent. In comparison with the adversarial agent trained by the state-of-the-art technique, we show that our adversarial agent exhibits a much stronger capability in exploiting the weakness of victim agents. Besides, we demonstrate that our adversarial attack introduces less variation in the training process and exhibits less sensitivity to the selection of initial states.

2. **[Justinian's GAAvernor: Robust Distributed Learning with Gradient Aggregation Agent](https://www.usenix.org/conference/usenixsecurity20/presentation/pan)**

    **Authors**: Xudong Pan, Mi Zhang, Duocai Wu, Qifan Xiao, Shouling Ji, Min Yang

    **Year**: 2020

    **Abstract**:

    The hidden vulnerability of distributed learning systems against Byzantine attacks has been investigated by recent researches and, fortunately, some known defenses showed the ability to mitigate Byzantine attacks when a minority of workers are under adversarial control. Yet, our community still has very little knowledge on how to handle the situations when the proportion of malicious workers is 50% or more. Based on our preliminary study of this open challenge, we find there is more that can be done to restore Byzantine robustness in these more threatening situations, if we better utilize the auxiliary information inside the learning process. 

    In this paper, we propose Justinian's GAAvernor (GAA), a Gradient Aggregation Agent which learns to be robust against Byzantine attacks via reinforcement learning techniques. Basically, GAA relies on utilizing the historical interactions with the workers as experience and a quasi-validation set, a small dataset that consists of less than $10$ data samples from similar data domains, to generate reward signals for policy learning. As a complement to existing defenses, our proposed approach does not bound the expected number of malicious workers and is proved to be robust in more challenging scenarios.

    Through extensive evaluations on four benchmark systems and against various adversarial settings, our proposed defense shows desirable robustness as if the systems were under no attacks, even in some case when 90% Byzantine workers are controlled by the adversary. Meanwhile, our approach shows a similar level of time efficiency compared with the state-of-the-art defenses. Moreover, GAA provides highly interpretable traces of worker behavior as by-products for further mitigation usages like Byzantine worker detection and behavior pattern analysis.

3. **[EcoFuzz: Adaptive Energy-Saving Greybox Fuzzing as a Variant of the Adversarial Multi-Armed Bandit](https://www.usenix.org/conference/usenixsecurity20/presentation/yue)**

    **Authors**: Tai Yue, Pengfei Wang, Yong Tang, Enze Wang, Bo Yu, Kai Lu, Xu Zhou

    **Year**: 2020

    **Abstract**:

    Fuzzing is one of the most effective approaches for identifying security vulnerabilities. As a state-of-the-art coverage-based greybox fuzzer, AFL is a highly effective and widely used technique. However, AFL allocates excessive energy (i.e., the number of test cases generated by the seed) to seeds that exercise the high-frequency paths and can not adaptively adjust the energy allocation, thus wasting a significant amount of energy. Moreover, the current Markov model for modeling coverage-based greybox fuzzing is not profound enough. This paper presents a variant of the Adversarial Multi-Armed Bandit model for modeling AFL’s power schedule process. We first explain the challenges in AFL's scheduling algorithm by using the reward probability that generates a test case for discovering a new path. Moreover, we illustrated the three states of the seeds set and developed a unique adaptive scheduling algorithm as well as a probability-based search strategy. These approaches are implemented on top of AFL in an adaptive energy-saving greybox fuzzer called EcoFuzz. EcoFuzz is examined against other six AFL-type tools on 14 real-world subjects over 490 CPU days. According to the results, EcoFuzz could attain 214% of the path coverage of AFL with reducing 32% test cases generation of that of AFL. Besides, EcoFuzz identified 12 vulnerabilities in GNU Binutils and other software. We also extended EcoFuzz to test some IoT devices and found a new vulnerability in the SNMP component.

#### International Conference on Software Engineering (1)

1. **[An automated framework for gaming platform to test multiple games](https://doi.org/10.1145/3377812.3382171)**

    **Authors**: Zihe Song

    **Year**: 2020

    **Abstract**:

    Game testing is a necessary but challenging task for gaming platforms. Current game testing practice requires significant manual effort. In this paper, we proposed an automated game testing framework combining adversarial inverse reinforcement learning algorithm with evolutionary multi-objective optimization. This framework aims to help gaming platform to assure market-wide game qualities as the framework is suitable to test different games with minimum manual customization for each game.
