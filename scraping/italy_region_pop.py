import numpy as np
import pandas as pd
from scipy.interpolate import InterpolatedUnivariateSpline as interpolate

pop = {}
pop['Liguria'] = np.array([109118,
                           128322,
                           138660,
                           151638,
                           223467,
                           252494,
                           203327,
                           189487,
                           154127])


pop['Abruzzo'] = np.array([104868,
117094,
134238,
156306,
196299,
203139,
167393,
129508,
102735])

pop['Lombardia'] = np.array([884414,
961237,
982354,
1187594,
1591034,
1566175,
1182159,
994236,
711371])

pop['Emilia-Romagna']=np.array([378176,
404912,
416656,
509891,
709189,
691144,
534643,
454624,
360242])

pop['Marche'] = np.array([123450,
138615,
148825,
172352,
230374,
233788,
191098,
156257,
130512])

pop['Piemonte'] = np.array([346338,
386792,
409014,
472194,
658299,
682253,
558840,
479555,
363121])

pop['Puglia'] = np.array([332668,
407564,
454334,
480448,
601316,
606678,
492806,
388850,
264389])

pop['Toscana'] = np.array([294910,
331182,
343614,
414568,
575674,
582074,
462876,
410421,
314322])

pop['Veneto'] = np.array([414926,
470462,
482384,
547052,
767625,
788986,
595088,
492166,
347165])

pop['Sardegna'] = np.array([116308,
138239,
158533,
193523,
260127,
266150,
223054,
170211,
113446])

xx = np.arange(10)*10+4.5
ages = np.arange(9)*10+4.5

colsave = ['region'] + ['%d'%i for i in range(10)]
df = pd.DataFrame(columns = colsave)

regions  = pop.keys()
for region in regions:
    yy = pop[region]
    vals = np.exp(interpolate(ages, np.log(yy))(xx))
    fac = yy [-1]/vals[-2:].sum()
    vals[-2:]*= fac
    tosave = np.array([region] + list(vals.astype(int))).reshape(1, -1)
    df = df.append(pd.DataFrame(tosave, columns=colsave), ignore_index=True)

    df.to_csv('../data/Italy/regional_popdist_fine.tsv', sep='\t', encoding='utf-8')
