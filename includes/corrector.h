#include <stdio.h>

void send_result(int num){
    printf("======result======\n");
    printf("%d\n", num);
    printf("====end=result====\n");
}

void send_message(char* msg){
    printf("======message======\n");
    printf("%s\n", msg);
    printf("====end=message====\n");
}