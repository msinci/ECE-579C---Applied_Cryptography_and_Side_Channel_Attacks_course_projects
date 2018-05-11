% flush&reload data analysis by MSI
clear all;
clc;

%vector =[99   124   119   123   242   107   111   197];
%T-table values from aes_core.c
vector =[99   124   119   123];

% data = zeros(100000,17);
data = textread('fnr_data/fnr_timings3');

num_traces=100000;

byte_no = 1;

for byte_no = 1:16

    for i=1:num_traces
        cbyte(i)=data(i,byte_no);
        reload_time(i)=data(i,17);
    end

    total=zeros(1,256);
    counter=zeros(1,256);
    ct_values=zeros(1,256);

    %For the first position of the ciphertext take corresponding timings
    for i=1:num_traces
        for j=0:255
            if cbyte(i)==j
                if reload_time(i)<500
                    ct_values(j+1)=ct_values(j+1)+1;
                    ct_timings(ct_values(j+1),j+1)=reload_time(i);
                end
            end
        end
    end

    %For all key candidates compute the Hyp0 and Hyp1 using mean distinguisher
    %method
    for key = 0 : 255
        % correct state hypothesis
        correct_state = bitxor(vector,key);
        % sum hypothesis
        ct_tsum = sum(ct_timings);
        ct_vsum = sum(ct_values);
        hyp0(key+1) = sum(sum(ct_timings(:,correct_state+1)))./sum(ct_values(correct_state+1));
        hyp1(key+1) = (sum(ct_tsum)-sum(sum(ct_timings(:,correct_state+1))))./(ct_vsum-sum(ct_values(correct_state+1)));
    end
    x=(0:255);
    %Find the difference between Hyp1 and Hyp0
    hypdifference=hyp1-hyp0;
    %Plot the difference and mark the correct key
%     figure;
    plot(x,hypdifference,'b')
    title(['byte ',num2str(byte_no),' hypothesis difference plot']);
    [val, idx] = max(hypdifference);
    result =['value of the last round key byte ', num2str(byte_no), ' is ',num2str(dec2hex(idx-1))];
    disp(result)
end
