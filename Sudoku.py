import itertools as it
import copy
import time
def Switch(I,J):# switches from x,y coordinates to box coordinates and from box coordinates to x,y coordinates
	return (I//3*3+J//3,I%3*3+J%3)
def Iterator(i,j,b,iterator):# (just a tool to help simplify my code) returns the iterator
	if iterator=="I":
		return i
	if iterator=="J":
		return j
	if iterator=="B":
		return b
def Check(table,i,j,version):# checks if further removal of candidates is avaliable
	if version==1:
		if len(table[i][j])==1:
			Naked1(table,i,j,1)
	if version==2:
		if len(table[i][j])==1:
			Naked1(table,i,j,2)
		else:
			k=0
			while k<9:
				Naked(k,table,i,-1,-1,2)
				Naked(k,table,-1,j,-1,2)
				Naked(k,table,-1,-1,Switch(i,j)[0],2)
				k+=1
			Pointing(table,i,-1,-1,2)
			Pointing(table,-1,j,-1,2)
			Pointing(table,-1,-1,Switch(i,j)[0],2)
def Naked1loop(table,i,j,iterator,version,target):# (just a tool to help simplify my code) helps Naked1
	b=[0]
	Iterator(i,j,b,iterator)[0]=0
	while Iterator(i,j,b,iterator)[0]<9:
		if iterator=="B":
			i=[Switch(Switch(i[0],j[0])[0],b[0])[0]]
			j=[Switch(Switch(i[0],j[0])[0],b[0])[1]]
		if len(table[i[0]][j[0]])!=1:
			oldlen=len(table[i[0]][j[0]])
			table[i[0]][j[0]]=table[i[0]][j[0]]-target
			if len(table[i[0]][j[0]])!=oldlen:
				Check(table,i[0],j[0],version)
		Iterator(i,j,b,iterator)[0]+=1
def Naked1(table,I,J,version):# removes the candidates that is in the same x,y,box when filling in a number
	target=table[I][J]
	Naked1loop(table,[I],[J],"I",version,target)
	Naked1loop(table,[I],[J],"J",version,target)
	Naked1loop(table,[I],[J],"B",version,target)
def Nakedloop(k,table,i,j,B,iterator,version):# (just a tool to help simplify my code) helps Naked
	b=[0]
	posI=[]
	posJ=[]
	bigset=set()
	Iterator(i,j,b,iterator)[0]=0
	while Iterator(i,j,b,iterator)[0]<9:
		if iterator=="B":
			i=[Switch(B,b[0])[0]]
			j=[Switch(B,b[0])[1]]
		if 1<len(table[i[0]][j[0]])<=k:
			posI.append(i[0])
			posJ.append(j[0])
			bigset=bigset.union(table[i[0]][j[0]])
		Iterator(i,j,b,iterator)[0]+=1
	if len(posI)>k:
		sets=it.combinations(bigset,k)
		for smallset in sets:
			smallset=set(smallset)
			count=0
			m=0
			while m<len(posI):
				if smallset.issuperset(table[posI[m]][posJ[m]])==True:
					count+=1
				m+=1
			if count==k:
				m=0
				while m<len(posI):
					if smallset.issuperset(table[posI[m]][posJ[m]])==False:
						oldlen=len(table[posI[m]][posJ[m]])
						table[posI[m]][posJ[m]]=table[posI[m]][posJ[m]]-smallset
						if len(table[posI[m]][posJ[m]])!=oldlen:
							Check(table,posI[m],posJ[m],version)
					m+=1
def Naked(k,table,I,J,B,version):# != -1 -> check this   # checks if naked k(which is hidden 9-k) has occurred in a specific x,y,box
	if I!=-1:
		Nakedloop(k,table,[I],[J],B,"J",version)
	if J!=-1:
		Nakedloop(k,table,[I],[J],B,"I",version)
	if B!=-1:
		Nakedloop(k,table,[I],[J],B,"B",version)
def Pointingloop(table,i,j,B,iterator,version,main):# (just a tool to help simplify my code) helps Pointing
	b=[0]
	posI=[]
	posJ=[]
	bigset={1,2,3,4,5,6,7,8,9}
	Iterator(i,j,b,iterator)[0]=0
	while Iterator(i,j,b,iterator)[0]<9:
		if iterator=="B":
			i=[Switch(B,b[0])[0]]
			j=[Switch(B,b[0])[1]]
		if len(table[i[0]][j[0]])==1:
			bigset=bigset-table[i[0]][j[0]]
		else:
			posI.append(i[0])
			posJ.append(j[0])
		Iterator(i,j,b,iterator)[0]+=1
	bigset=tuple(bigset)
	m=0
	while m<len(bigset):
		rowset=set()
		colset=set()
		boxset=set()
		n=0
		while n<len(posI):
			if table[posI[n]][posJ[n]].issuperset({bigset[m]})==True:
				rowset.add(posI[n])
				colset.add(posJ[n])
				boxset.add(Switch(posI[n],posJ[n])[0])
			n+=1
		if main=="I" or main=="J":
			Pointingloopp(table,i[0],j[0],B,"B",version,bigset,boxset,main,m)
		if main=="B":
			Pointingloopp(table,i[0],j[0],B,"J",version,bigset,rowset,main,m)
			Pointingloopp(table,i[0],j[0],B,"I",version,bigset,colset,main,m)
		m+=1
def Pointingloopp(table,I,J,B,iterator,version,bigset,sett,main,m):# (just a tool to help simplify my code) helps Pointing
	if len(sett)==1:
		sett=tuple(sett)
		i=[sett[0]]
		j=[sett[0]]
		b=[0]
		Iterator(i,j,b,iterator)[0]=0
		while Iterator(i,j,b,iterator)[0]<9:
			if iterator=="B":
				i=[Switch(sett[0],b[0])[0]]
				j=[Switch(sett[0],b[0])[1]]
			if Iterator(i,j,[Switch(i[0],j[0])[0]],main)[0]!=Iterator(I,J,B,main) and len(table[i[0]][j[0]])!=1:
				oldlen=len(table[i[0]][j[0]])
				table[i[0]][j[0]]=table[i[0]][j[0]]-{bigset[m]}
				if len(table[i[0]][j[0]])!=oldlen:
					Check(table,i[0],j[0],version)
			Iterator(i,j,b,iterator)[0]+=1
def Pointing(table,I,J,B,version):# != -1 -> check this   # checks if pointing has occurred in a specific x,y,box
	if I!=-1:
		Pointingloop(table,[I],[J],B,"J",version,"I")
	if J!=-1:
		Pointingloop(table,[I],[J],B,"I",version,"J")
	if B!=-1:
		Pointingloop(table,[I],[J],B,"B",version,"B")
def PrintTable(table):# prints the table
	i=0
	while i<9:
		j=0
		while j<9:
			if len(table[i][j])==1:
				print(tuple(table[i][j])[0],end="")
			else:
				print(" ",end="")
			j+=1
		print()
		i+=1

que=((0,0,0,0,0,0,0,1,5)
	,(0,2,0,0,6,0,0,0,0)
	,(0,0,0,0,0,0,4,0,8)
	,(0,0,3,0,0,0,9,0,0)
	,(0,0,0,1,0,0,0,0,0)
	,(0,0,0,0,0,8,0,0,0)
	,(1,5,0,4,0,0,0,0,0)
	,(0,0,0,0,7,0,3,0,0)
	,(8,0,0,0,0,0,0,6,0))

table=[]# makes the table and inputs
i=0
while i<9:
	table.append([])
	j=0
	while j<9:
		table[i].append({1,2,3,4,5,6,7,8,9})
		j+=1
	i+=1
i=0
while i<9:
	inp=que[i]
	if i==0:
		start=time.time()
	j=0
	while j<9:
		if inp[j]!=0:
			table[i][j]={int(inp[j])}
			Naked1(table,i,j,1)
		j+=1
	i+=1
i=0# first scan
while i<9:
	j=2
	while j<9:
		Naked(j,table,i,-1,-1,2)
		Naked(j,table,-1,i,-1,2)
		Naked(j,table,-1,-1,i,2)
		j+=1
	Pointing(table,i,-1,-1,2)
	Pointing(table,-1,i,-1,2)
	Pointing(table,-1,-1,i,2)
	i+=1
def Solve(table):# checks if the table is solved or stuck or erroneous
	boolean=True
	i=0
	while i<9:
		j=0
		while j<9:
			if len(table[i][j])!=1:
				boolean=False
			j+=1
		i+=1
	if boolean==True:# solved
		end=time.time()
		PrintTable(table)
		return end
	else:# stuck
		I=0
		while I<9:
			J=0
			while J<9:
				if len(table[I][J])!=1:
					candidates=tuple(table[I][J])
					correcttable=copy.deepcopy(table)
					K=0
					while K<len(candidates):
						table[I][J]={candidates[K]}# guesses one number from the candidates
						Naked1(table,I,J,2)
						boolean=True
						k=0
						while k<9:
							i=0
							while i<9:
								count=0
								j=0
								while j<9:
									if table[i][j]=={k}:
										count+=1
									j+=1
								if count>1:
									boolean=False
								i+=1
							j=0
							while j<9:
								count=0
								i=0
								while i<9:
									if table[i][j]=={k}:
										count+=1
									i+=1
								if count>1:
									boolean=False
								j+=1
							B=0
							while B<9:
								count=0
								b=0
								while b<9:
									tempI=Switch(B,b)[0]
									tempJ=Switch(B,b)[1]
									if table[tempI][tempJ]=={k}:
										count+=1
									b+=1
								if count>1:
									boolean=False
								B+=1
							k+=1
						if boolean==False:# erroneous
							table=copy.deepcopy(correcttable)
						else:
							result=Solve(table)
							if result==False:# erroneous
								table=copy.deepcopy(correcttable)
							else:# solved
								return result
						K+=1
					return False
				J+=1
			I+=1
print("Question:")
i=0
while i<9:
	j=0
	while j<9:
		print(que[i][j],end="")
		j+=1
	print()
	i+=1
print()
print("Answer:")
end=Solve(table)
print()
print(end-start,"s",sep="")