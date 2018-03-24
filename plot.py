import matplotlib.pyplot as plt
#casual 
plt.plot([5, 10, 20, 50, 100], [5.29, 5.27, 5.63, 13.31, 28.47], "r--", label = 'Causal Ordering')
plt.plot([5, 10, 20, 50, 100], [5.26, 5.38, 5.65, 5.67, 30.76], "g--", label = 'FIFO Ordering')
plt.plot([5, 10, 20, 50, 100], [13.56, 11.69, 20.1, 50.22, 100.50], "b--", label = 'Total Ordering')
plt.legend(loc='upper left')
plt.ylabel('Total Deliver time(s)')
plt.xlabel('Number of message per node')
plt.show()