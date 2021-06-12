# Made by @Saksham Solanki, Date: 03/04/2021 (DD/MM/YYYY) Time: 20:57 (24-hour-format)
# Importing all libraries to be used.
import tkinter as tk
import pandas as pd
from scipy.sparse import csr_matrix #pip3 install scipy
from sklearn.neighbors import NearestNeighbors #pip3 install sklearn
from selenium import webdriver #pip3 install selenium
from googlesearch import search #pip3 install google
import os

# Importing the data file which contains all of the inputs regarding movies
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# Reading the ratings, movieID and userID of all movies present
final_dataset = ratings.pivot(index='movieId',columns='userId',values='rating')
final_dataset.fillna(0,inplace=True)

# Regrouping all non voted movies
no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
no_movies_voted = ratings.groupby('userId')['rating'].agg('count')

# Removing all non voted movies as well as movies with reviews less than 50
final_dataset=final_dataset.loc[:,no_movies_voted[no_movies_voted > 50].index]

# converting our dataset into a csr_matrix val to initialize it for our algorithm
csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)

# Using the KNN algorithm to calculate the distance between movies (comparing them)
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(csr_data)
num_of_title = -1
# Last function to getting the recommeded movie from our perfectly refined dataset
def movie_recommendation(movie_name):
    titles = []
    n_movies_to_recommend = 10
    movie_list = movies[movies['title'].str.contains(movie_name)]  
    if len(movie_list):        
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        
        distances , indices = knn.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_recommend+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),\
                               key=lambda x: x[1])[:0:-1]
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            Title = movies.iloc[idx]['title'].values[0]
            titles.append(Title)

        def show_about_movie():
            query = titles[(num_of_title-1)]
            path = os.getcwd()
            link = ""
            if os.name == 'nt':
                driver = webdriver.Chrome(executable_path=path+"/w_chromedriver.exe")
            elif os.name == 'posix':
                driver = webdriver.Chrome(executable_path=path+"/chromedriver")
            else:
                print("Your device is not compatible")
            for j in search(query,tld="co.in",num=10,stop=10,pause=1):
                if "image" not in j or ".jpg" not in j or ".png" not in j:
                    link = j
                    break
            driver.get(link)

        def left_b():
            global num_of_title
            num_of_title -= 1
            if num_of_title < 10 and num_of_title >= 0:
                label = len(titles[num_of_title])
                if label > 25 and label < 35:
                    Label.config(text=titles[num_of_title],bg="#228699")
                    Label.place(relx = 0.3, rely=0.4)
                elif label > 40 and label < 52:
                    Label.config(text=titles[num_of_title],bg="#228699")
                    Label.place(relx = 0.2, rely=0.4)
                elif label > 52:
                    Label.config(text=titles[num_of_title],bg="#228699")
                    Label.place(relx = 0.1, rely=0.4)
                else:
                    Label.config(text=titles[num_of_title], bg="#228699")
                    Label.place(relx=0.4,rely=0.4)
            else:
                num_of_title = -1

        def right_b():
            global num_of_title
            if num_of_title < 10 and num_of_title >= 0:
                label = len(titles[num_of_title])
                if label > 25 and label < 35:
                    Label.config(text=titles[num_of_title],bg="#228699")
                    Label.place(relx = 0.3, rely=0.4)
                elif label > 40 and label < 52:
                    Label.config(text=titles[num_of_title],bg="#228699")
                    Label.place(relx = 0.2, rely=0.4)
                elif label > 52:
                    Label.config(text=titles[num_of_title],bg="#228699")
                    Label.place(relx = 0.1, rely=0.4)
                else:
                    Label.config(text=titles[num_of_title], bg="#228699")
                    Label.place(relx=0.4,rely=0.4)
            else:
                num_of_title = -1

        def print_titles():
            global num_of_title
            if num_of_title < 10:
                label = len(titles[num_of_title])
                if label > 25 and label < 35:
                    Label.config(text=titles[num_of_title],bg="#228699")
                    Label.place(relx = 0.3, rely=0.4)
                elif label > 40 and label < 52:
                    Label.config(text=titles[num_of_title],bg="#228699")
                    Label.place(relx = 0.2, rely=0.4)
                elif label > 52:
                    Label.config(text=titles[num_of_title],bg="#228699")
                    Label.place(relx = 0.1, rely=0.4)
                else:
                    Label.config(text=titles[num_of_title], bg="#228699")
                    Label.place(relx=0.4,rely=0.4)
            else:
                num_of_title = -1
            num_of_title += 1
            window_1.after(3000, print_titles)
        window_1 = tk.Tk()
        window_1.title("Recommended Movies")
        window_1.geometry("700x500")
        j = 0
        r = 200
        for i in range(8):
            c = str(228499+r) 
            tk.Frame(window_1, width=200, height=800, bg="#"+c).place(x=j, y=0)
            j += 200
            r += 400
            i = i
        left = tk.PhotoImage(file="left.png")
        button_1 = tk.Button(window_1,image=left, command=lambda:[left_b()])
        button_1.place(relx=0.02,rely=0.39)
        right = tk.PhotoImage(file="right.png")
        button_2 = tk.Button(window_1, image=right, command=lambda:[right_b()])
        button_2.place(relx=0.9,rely=0.39)
        Label = tk.Label(text=titles[num_of_title], font=("Aerial",13),bg="#228699", foreground="white")
        show_more = tk.Button(text="About Movie", foreground="white",bg="#228699", command=lambda:[show_about_movie()])
        show_more.place(relx=0.43,rely=0.5)
        Label.place(relx=0.4,rely=0.4)
        print_titles()
        window_1.mainloop()
    else:
        print("No movies found. Please check your input")

def name():
    movie_name = str(entry1.get())
    window_0.destroy()
    movie_recommendation(movie_name)

window_0 = tk.Tk()
window_0.title("Recommendinator")
canvas1 = tk.Canvas(window_0, width = 400, height = 300)
canvas1.pack()
entry1 = tk.Entry (window_0)
canvas1.create_window(200, 140, window=entry1)
button1 = tk.Button(text = "Enter Movie Name", command=lambda:[name()])
canvas1.create_window(200, 180, window=button1)
window_0.mainloop()