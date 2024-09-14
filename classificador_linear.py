import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def main(epochs, accuracy):
    print(f"epochs: {epochs}")
    print(f"accuracy: {accuracy}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("epochs", type=int, help="numero de epocas")
    parser.add_argument("accuracy", type=float, help="acuracia desejada")
    
    args = parser.parse_args()
    main(args.epochs, args.accuracy)

# Load data from CSV file
df = pd.read_csv('dogs_cats.csv')  

print(df.head())


cats = df[df['classe'] == 'gato']
dogs = df[df['classe'] == 'cachorro']
x_cats,y_cats = cats['peso'],cats['comprimento']
x_dogs,y_dogs = dogs['peso'],dogs['comprimento']  


def classificador_linear(epochs=args.epochs,X=df,accur=args.accuracy):
    
    acc,acc_old= 0, 0
    a,b=0,0
    ref_a,ref_b=0,0
    
    for i in range(0,epochs):
        acertos_cats,acertos_dogs = 0,0
        if i==0:
            a, b = np.polyfit(X['peso'],X['comprimento'],1)
            a=round(a,3)
            b=round(b,3)
            x_vals = np.arange(200, len(cats)-200, 1)  
            y_vals = a * x_vals + b

            pares_xy = np.column_stack((x_vals, y_vals))
            for value in pares_xy:
                begin = value[0] 
                end = value[0] + 1
                cats_found = [id for id,x in enumerate(x_cats) if begin <= x <= end]
                dogs_found = [id for id,x in enumerate(x_dogs) if begin <= x <= end]
               
                for id in cats_found:
                    if x_cats.iloc[id] < value[0] and y_cats.iloc[id] < value[1]:
                        acertos_cats +=1
                #print(acertos_cats)
                for id in dogs_found:
                    #print(x_dogs.iloc[id], y_dogs.iloc[id], value[0],value[1])
                    if x_dogs.iloc[id] > value[0] and y_dogs.iloc[id] > value[1]:
                        #print(acertos_dogs)
                        acertos_dogs +=1
            print(acertos_cats,acertos_cats)
            acc = (acertos_cats+acertos_dogs)/len(X)
            acc_old = acc
            ref_a,ref_b=a,b
        else:
            b = b - 1
            y_vals = a * x_vals + b
            
            acertos_cats,acertos_dogs = 0,0
            pares_xy = np.column_stack((x_vals, y_vals))
             
            for value in pares_xy:
                
                begin = value[0]
                end = value[0] + 1
                
                cats_found = [id for id,x in enumerate(x_cats) if begin <= x <= end]
                dogs_found = [id for id,x in enumerate(x_dogs) if begin <= x <= end]
                   
                for id in cats_found:
                    if x_cats.iloc[id] < (value[0]+1) and y_cats.iloc[id] < value[1]:
                        acertos_cats +=1
                for id in dogs_found:
                   
                    if x_dogs.iloc[id] > value[0] and y_dogs.iloc[id] > value[1]:
                        
                        acertos_dogs +=1
                acc = (acertos_cats+acertos_dogs)/len(X)
            

           
            a = a + 0.01 
           
            y_vals = a * x_vals + b
            pares_xy = np.column_stack((x_vals, y_vals))
            acertos_cats,acertos_dogs = 0,0
            for value in pares_xy:
                begin = value[0] 
                end = value[0] + 1
                cats_found = [id for id,x in enumerate(x_cats) if begin <= x <= end]
                dogs_found = [id for id,x in enumerate(x_dogs) if begin <= x <= end]
                
                for id in cats_found:
                    if x_cats.iloc[id] < (value[0]+1) and y_cats.iloc[id] < value[1]:
                        acertos_cats +=1
               
                for id in dogs_found:
                     if x_dogs.iloc[id] > value[0] and y_dogs.iloc[id] > value[1]:
                        acertos_dogs +=1   
            #print(acc, acertos_dogs)
            acc = (acertos_cats+acertos_dogs)/len(X)
            #print("\na:", acc_old,acc)

            if acc < acc_old:
                a = a - 0.01
                #b=b+1
            elif acc > acc_old:
                ref_a = a
                ref_b=b
                acc_old = acc

            print("\n-------\nepochs:", i,"\nacuracia:", acc,"\nacuracia old:", acc_old,"\na:",ref_a,"\nb:", ref_b,"\nacertos:", acertos_cats,acertos_dogs)
        if acc >= accur:
            break
    
    return ref_a, ref_b, acc

a,b,acc = classificador_linear(args.epochs,df,args.accuracy)
#print(acc)

plt.figure(figsize=(8, 6))
x = np.linspace(0, 1000, 1000) 

# Equação da reta
y = a * x + b

##print((a*200)+b)
plt.plot(x, y, label=f"y = {a}x + {b}")
plt.scatter(cats['peso'], cats['comprimento'], color='blue', label='Cats', marker='o')
plt.scatter(dogs['peso'], dogs['comprimento'], color='green', label='Dogs', marker='x')

plt.xlabel('Peso')
plt.ylabel('Comprimento')
plt.title('Plot')
plt.legend()

plt.show()
