import tailer
for line in tailer.follow(open('kareem.log')):
    print(line)