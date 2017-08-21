#coding: utf-8

def startend(totalnum, perpagenum):
	if totalnum % perpagenum == 0:
		pages = int(totalnum)/int(perpagenum)
	else:
		pages = int(totalnum)/int(perpagenum) + 1
	displayRange = []
	for i in range(pages):
		start = i * perpagenum
		end = (i + 1) * perpagenum
		if end > totalnum:
			end = totalnum
		displayRange.append([start, end])
	return displayRange