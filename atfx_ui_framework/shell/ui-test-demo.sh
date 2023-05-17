#！/bin/bash
### 需要跑的测试流程
cat /dev/null > report_list.txt
### 需要跑的测试流程
echo '您输入的FLOW_NAME为:'$FLOW_NAME

# 根据输入的FLOW_NAME运行相应的流程
# 比如输入’1‘，会执行 1）后面所对应的脚本，以此类推
# 如果什么都不输入则会执行*）后面所对应的脚本
runAutotest(){
    case $FLOW_NAME in
        1)  echo 'You select 1'
            python demo/change_psword/action_bin/change_password_cp.py
        ;;
        2)  echo 'You select 2'
            python demo/withdrawal/withdrawal_bin/test_withdrawal_cp_bin.py
        ;;
        3)  echo 'You select 3'
        ;;
        *)  
            echo 'Running all test flow'
            python demo/run_main_process.py
        ;;
    esac
}

runAutotest
### 通过msteams发送测试报告
python demo/public/ms_teams.py

