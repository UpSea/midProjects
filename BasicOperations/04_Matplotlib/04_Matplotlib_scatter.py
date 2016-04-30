import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(10,2), columns=['col1','col2'])
df['col3'] = np.arange(len(df))**2 * 100 + 100


plt.scatter(df.col1, df.col2, s=df.col3)



df['subset'] = np.select([df.col3 < 150, df.col3 < 400, df.col3 < 600],
                         [0, 1, 2], -1)
for color, label in zip('bgrm', [0, 1, 2, -1]):
    subset = df[df.subset == label]
    plt.scatter(subset.col1, subset.col2, s=120, c=color, label=str(label))
plt.legend()


plt.show()