import glob
import hashlib
import os
import csv

# Bulk MD5 File Compare - Created by Jace Voracek
# Compare files between two directories to determine which files are unique. Also records each files' MD5 hash to a CSV file.



# CHANGE THESE FOUR DIRECTORY PATHS! 
# Unique files will be moved to each respective uniqueFilesOutputDir directory. Non-unique files will be left in their respective srcDir directory.

srcDir1 = "/example/firstDirectoryToCompare/*"
srcDir2 = "/example/secondDirectoryToCompare/*"

uniqueFilesOutputDir1 = "/example/directoryWhereUniqueDir1FilesWillGo/"
uniqueFilesOutputDir2 = "/example/directoryWhereUniqueDir2FilesWillGo/"








filenames = glob.glob(srcDir1)
filenames2 = glob.glob(srcDir2)

targetDir1 = uniqueFilesOutputDir1
targetDir2 = uniqueFilesOutputDir2

arr1 = []
arr2 = []

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(2 ** 20), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()




#Get MD5s for each filename

for filename in filenames:
    print(filename, md5(filename))
    arr1.append([filename, md5(filename)])

for filename in filenames2:
    print(filename, md5(filename))
    arr2.append([filename, md5(filename)])



#Find collision with MD5s

d1 = {sub[1]: sub for sub in arr1}
d2 = {sub[1]: sub for sub in arr2}

finalArray1 = [d2[k] for k in d2.keys() - d1]
finalArray2 = [d1[k] for k in d1.keys() - d2]



#Move files that are in the final array

start = "['"
end = "',"

for item in finalArray1:
    s = str(item)
    path = ((s.split(start))[1].split(end)[0])
    os.rename(str(path), (targetDir1 + os.path.basename(str(path))))

for item in finalArray2:
    s = str(item)
    path = ((s.split(start))[1].split(end)[0])
    os.rename(str(path), (targetDir2 + os.path.basename(str(path))))

#Get remaining files and try to pair them

arr3 = []
arr4 = []




#Get MD5s for each filename

test1 = glob.glob(srcDir1)
tgtDir1 = glob.glob(targetDir1 + "*") 

for filename1 in test1:
    print("same1: ", filename1, md5(filename1))
    arr3.append([filename1, md5(filename1)])

test2 = glob.glob(srcDir2) 
tgtDir2 = glob.glob(targetDir2 + "*") 

for filename2 in test2:
    print("Filename: ", filename2)
    print("same2: ", filename2, md5(filename2))
    arr4.append([filename2, md5(filename2)])


#Write to file

with open("notUniqueFromSrcDir1.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(arr3)

with open("notUniqueFromSrcDir2.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(arr4)



#Get unique files and try to pair them

arr5 = []
arr6 = []

#Get MD5s for each filename

for filename in tgtDir1:
    print("unique1: ", filename, md5(filename))
    arr5.append([filename, md5(filename)])

for filename in tgtDir2:
    print("unique2: ", filename, md5(filename))
    arr6.append([filename, md5(filename)])

#Write to file

with open("uniqueFromSrcDir1.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(arr5)

with open("uniqueFromSrcDir2.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(arr6)


print("Finished :-)")
