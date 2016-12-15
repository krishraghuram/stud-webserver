#All app(tau) level constants are defined here for easy modification

# total_drive_space = 268435456 #250 MibiBytes = 250*1024*1024 Bytes
total_drive_space = 1024*1024*250 #250MibiBytes
#Need to implement max_filesize in apache. Coz when django is checking for filsize, file is long uploaded.
#max_filesize = 1024*1024*25 #25MibiBytes
max_subfolders = 10
max_folder_depth = 7