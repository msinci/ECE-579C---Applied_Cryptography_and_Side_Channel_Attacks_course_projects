% temp2 

clear all
% close all
%vector =[99   124   119   123   242   107   111   197];
%Find the T-table values from aes_core.c
vector =[99   124   119   123];
%Get the data from .txt file
t=load('fnr_data/fnr_timings3');
%Extract the data from .txt file

num_traces=100000;

for i=1:num_traces
    ciphertext0(i)=t(i,1);
    reload0(i)=t(i,17);
end

total=zeros(1,256);
counter=zeros(1,256);
counter2=zeros(1,256);

%For the first position of the ciphertext take corresponding timings
for i=1:num_traces
    for j=0:255
        if ciphertext0(i)==j
            if reload0(i)<500
                counter2(j+1)=counter2(j+1)+1;
                table3(counter2(j+1),j+1)=reload0(i);
            end
        end
    end
end

%For all key candidates compute the Hyp0 and Hyp1 using mean distinguisher
%method
for key = 0 : 255
    % compute correct
    correct = bitxor(vector,key);
    % sum hyp
    RlThyp0(key+1) = sum(sum(table3(:,correct+1)))./sum(counter2(correct+1));
    RlThyp1(key+1) = (sum(sum(table3))-sum(sum(table3(:,correct+1))))./(sum(counter2)-sum(counter2(correct+1)));
end
x=[0:255];
%Find the difference between Hyp1 and Hyp0
mean=RlThyp1-RlThyp0;
%Plot the difference and mark the correct key
figure;
plot(x,mean,'r')