% Collision attack data analysis by MSI
clearvars -except timings;
clc;
load('ca_data.mat', 'timings')


num_traces=500000;
firstbyte = 11;
secondbyte = 12;
bin = zeros(256,1);
cnt = zeros(256,1);

for dataset = 1:10
    dataset
    NAME = strcat('ca_tada/ca_data',num2str(dataset));
                ciphertext = textread(NAME);
    timings(dataset,:,:) = ciphertext(:,1:17);
    for trace = 1:num_traces
        delta = bitxor(ciphertext(trace,firstbyte),ciphertext(trace,secondbyte));
        if ciphertext(trace,17)<1000
            bin(delta+1) = bin(delta+1) + ciphertext(trace,17);
            cnt(delta+1) = cnt(delta+1) + 1;
        end
    end
end

for index = 1:256
    bin(index) = bin(index)/cnt(index);
end

plot(bin)

key = [hex2dec('b4'), hex2dec('ef'), hex2dec('5b'), hex2dec('cb'), hex2dec('3e'), hex2dec('92'), hex2dec('e2'), hex2dec('11'), hex2dec('23'), hex2dec('e9'), hex2dec('51'), hex2dec('cf'), hex2dec('6f'), hex2dec('8f'), hex2dec('18'), hex2dec('8e')];
delta = bitxor(key(firstbyte), key(secondbyte));
[val, pos] = min(bin);

if pos==delta+1
    ['Correct delta is: ',num2str(dec2hex(delta))]
else
    temppos=pos+1
    ['%d is not the correct delta. maybe need more samples?',temppos]
end
hold on
plot(delta+1,bin(delta+1),'+r')
hold off

