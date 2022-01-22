
def function(low, high):
    num_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    low_len = len(str(low))
    res = []
    high_len = len(str(high))
    for length in range(low_len, high_len+1):
        for index in range(0, 10-length):
            s_index = index
            s_length = length
            num_str = ''
            while s_length:
                num_str += num_list[s_index]
                s_length -= 1
                s_index += 1
            if low <= int(num_str) <= high:
                res.append(int(num_str))
            continue
    return res

if __name__ == '__main__':
    print(function(1000, 13000))