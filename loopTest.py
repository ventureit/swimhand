# import time
# import datetime
#
# struct_time1 = datetime.datetime.strptime('15:36:03', '%X').strftime('%H:%M:%S')
# struct_time2 = datetime.datetime.strptime('15:38:03', '%X').strftime('%H:%M:%S')
# # print('returned tuple: %s ' % struct_time2 - struct_time1)
# a = struct_time2 - struct_time1

import datetime
import time
start_time = datetime.datetime.strptime('15:36:03', '%X') #.strftime('%H:%M:%S')
end_time = datetime.datetime.strptime('15:38:03', '%X') #.strftime('%H:%M:%S')
total_time = end_time - start_time
print(total_time.total_seconds())