import numpy as np
import matplotlib.pyplot as plt


# Range of LOGMAR values we'll test in MNREAD
start=-0.2
interval = 0.1
n=12

logmar_vals=list(np.round(np.arange(start, interval * n , interval),2))

vis_degree_vals=[round(0.083*(10**i),3) for i in logmar_vals]

print(logmar_vals)
print(vis_degree_vals)

plt.scatter(logmar_vals, vis_degree_vals, color='red', label='Data Points')
plt.xticks(logmar_vals)
plt.yticks(vis_degree_vals,rotation=45)
plt.xlabel('logMAR')
plt.ylabel('Visual Degree')
plt.title('Logmar to Visual Degree')
plt.legend()
plt.show()

