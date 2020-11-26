from matplotlib import pyplot as plt

def make_fig():
    with open('loss.txt', 'r') as f:
        data = f.readlines()

    datas = [float(num.replace('\n', '')) for num in data]
    x = list(range(len(datas)))
    plt.plot(x,datas)
    plt.savefig('loss.png')


if __name__ == "__main__":
    make_fig()