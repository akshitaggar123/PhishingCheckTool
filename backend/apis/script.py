'''import random
afile = open("querydata.txt", "w" )

n=600
line=''
for i in range(n-1):
     line=line+str(random.randint(1,500))+' '
line=line+str(random.randint(1,500))
afile.write(line)
    #print(line)

afile.close()'''

def bubbleSort(arr):
    n = len(arr)
   
    # Traverse through all array elements
    for i in range(n):
        swapped = False
  
        # Last i elements are already
        #  in place
        for j in range(0, n-i-1):
   
            # traverse the array from 0 to
            # n-i-1. Swap if the element 
            # found is greater than the
            # next element
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
  
        # IF no two elements were swapped
        # by inner loop, then break
        if swapped == False:
            break

def binarySearch (arr, l, r, x):
  
    # Check base case
    if r >= l:
  
        mid = l + (r - l) // 2
  
        # If element is present at the middle itself
        if arr[mid] == x:
            return mid
          
        # If element is smaller than mid, then it 
        # can only be present in left subarray
        elif arr[mid] > x:
            return binarySearch(arr, l, mid-1, x)
  
        # Else the element can only be present 
        # in right subarray
        else:
            return binarySearch(arr, mid + 1, r, x)
  
    else:
        # Element is not present in the array
        return -1

line="195 433 443 309 376 88 31 188 260 231 407 177 285 371 106 213 244 314 210 352 449 125 223 127 225 255 342 181 349 86 197 409 248 239 353 245 422 14 413 155 93 189 252 483 383 477 453 240 158 452 388 450 248 103 62 247 469 377 16 243 2 300 397 330 485 456 266 82 116 477 253 500 288 23 484 22 431 65 409 162 318 348 106 64 246 42 344 175 250 496 91 454 232 33 57 421 313 166 433 443 129 426 252 211 255 440 87 126 168 233 480 223 305 59 309 364 68 121 376 252 191 317 384 48 271 27 176"
arr=line.split()

for i in range(len(arr)):
    arr[i]=int(arr[i])
    if(arr[i]==309):
        print("yes")

bubbleSort(arr)
pos=binarySearch(arr, 0, len(arr)-1, 309)
print(pos)



