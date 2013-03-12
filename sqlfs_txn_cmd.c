#include <sys/types.h>
#include <sys/xattr.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define DB_START_TRANS_XATTR_NAME "full_db_transaction_start"
#define DB_STOP_TRANS_XATTR_NAME "full_db_transaction_stop"
#define DB_RB_TRANS_XATTR_NAME "full_db_transaction_rb"
#define DB_TRANS_ONLY_CHECK "full_db_transaction_check"

int main(int argc, char** argv)
{
	int pid;

	pid = getpid();
	if(argc < 3){
		printf("%s <path> <cmd>\n", argv[0]);
		printf("ex) %s /opt/var/kdb/db \"cp -a db_bak/* db\"\n", argv[0]);
		return -1;
	}

	if(setxattr(argv[1], DB_START_TRANS_XATTR_NAME, &pid, sizeof(pid), 0) == -1)
		printf("start failed\n");

	system(argv[2]);

	if(setxattr(argv[1], DB_STOP_TRANS_XATTR_NAME, &pid, sizeof(pid), 0) == -1)
		printf("stop failed\n");

	sync();

	return 0;
} 
