class Pattern:
    def __init__(self, file_name):
        self.pattern = []
        with open(file_name) as f:
            for line in f:
                if line != "\n":
                    self.pattern.append(line.rstrip())
        self.pattern_num = [0] * len(self.pattern)

    def update_pattern_num(self, board):
        self.pattern_num = [0] * len(self.pattern)
        for row in range(15):
            for col in range(15):
                for length in range(len(self.pattern_num)):
                    is_add = True
                    for index in range(7):
                        if col + index < 15:
                            if self.pattern[length][index] != '.' and board[row][col + index] != self.pattern[length][index]:
                                is_add = False
                            #A black white threshhold
                            if length < 11 and self.pattern[length][index] == '.' and board[row][col + index] == 'b':
                                is_add = False
                        else:
                            is_add = False
                    if is_add:
                        self.pattern_num[length] = self.pattern_num[length] + 1
        #print(self.pattern_num)

#pattern = Pattern("pattern.txt")
