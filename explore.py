# create a function that takes in a dataframe
def plot_variable_pairs(df):
    # plot the columns in a pairplot
    sns.pairplot(train, kind = 'reg', corner = True, plot_kws={'line_kws':{'color':'red'}})
    plt.show()