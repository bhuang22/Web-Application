

def movingjobs(l,h):
    matrixL=[0 for x in range(len(l))]
    matrixH=[0 for x in range(len(h))]

    matrixL[0]=l[0]
    matrixH[0]=h[0]

    for i in range(1,len(l)):
        matrixL[i]=max(matrixL[i-1]+l[i],l[i]+matrixH[i-1])
        matrixH[i]=max(h[i]+matrixL[i-2], h[i]+matrixH[i-2])
        print(matrixL,matrixH)
        print("current revenue")
        print(matrixL[i],matrixH[i])
        print("compare low")
        print(matrixL[i-1]+l[i],l[i]+matrixH[i-1])
        print("compare high")
        print(h[i]+matrixL[i-2], h[i]+matrixH[i-2])



    print(matrixL)   
    print(matrixH)

    print("result:")
    print(max(matrixH[-1],matrixL[-1]))


if __name__ == '__main__':
    l=[10,1,10,10]
    h=[5,50,70,1]

    movingjobs(l,h)
