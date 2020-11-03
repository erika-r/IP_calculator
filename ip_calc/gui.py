
from tkinter import *
from ip_calc import *

def button_click(entry):
	query = [str(word) for word in entry.split(",")]
	func = query[-1]

	success = True
	if func == "cs":
		output = get_class_stats(query[0])
	elif func == "subnet":
		output = get_subnet_stats(query[0],query[1])
	elif func == "supernet":	#take in string and make into list
		output = get_supernet_stats(query[:-1])
	else:
		success = False
		output = "Invalid/No function, try again"

	if success:
		results_label["fg"] = "black"
		results_label["wraplength"]=350
		results_label["anchor"]="w"
		results_label["justify"]=LEFT,
	else:
		results_label["fg"] = "#660000"
	
	results_label["text"] = output

window = Tk()
window.title("IP Calculator")
window.resizable(False,False)

#canvas fills whole screen
canvas = Canvas(window,height=600,width=500,bg="#333333")
canvas.pack(fill="both",expand=True)

#top frame - for button and input
frame = Frame(window,bg="#FFD55A",bd=5)
frame.place(relx=0.5,rely=0.1,relwidth=0.75,relheight=0.1,anchor="n")

#input box
entry = Entry(frame,bg="#ffffff",font=40)
entry.place(relwidth=0.65,relheight=1)

#enter button
button = Button(frame,text="calculate",bg="#FFD55A",font=("Fixedsys",10),command=lambda: button_click(entry.get()))	#get input from entry box, lambda allows button to be clicked again
button.place(relx=0.7,relheight=1,relwidth=0.3)


#middle frame - for results
results_frame = Frame(window,bd=5,bg="black")
results_canvas = Canvas(results_frame,bg="white")

#scrollbar for results frame
scrollbar = Scrollbar(results_frame,orient="vertical",command=results_canvas.yview)
scrollable_frame = Frame(results_canvas)
scrollable_frame.bind("<Configure>",lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all")))

results_canvas.create_window((0,0),window=scrollable_frame)
results_canvas.configure(yscrollcommand=scrollbar.set)

results_label = Label(scrollable_frame,text="Results will appear here",fg="gray",font=("Fixedsys",9),bg="white")
results_label.pack()	#takes up entire space

results_frame.place(relx=0.1,rely=0.25,relwidth=0.8)
results_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


#bottom frame - instructions for input
instructions_frame = Frame(window,bg="#660000",bd=10)
instructions_frame.place(relx=0.5,rely=0.95,relwidth=0.75,relheight=0.2,anchor="s")

desc = "Input Method:\nClass Statistics = *ip address*,cs\nSubnet Statistics = *ip address*,*subnet mask*,subnet\nSupernet Statistics = *ip address 1*,*ip address 2*, . . .,supernet"
instructions_label = Label(instructions_frame,text=desc,justify=CENTER,font=("Fixedsys",7,"bold"),bg="white",bd=4,wraplength=250)
instructions_label.place(relwidth=1,relheight=1)	#takes up entire space

window.mainloop()
