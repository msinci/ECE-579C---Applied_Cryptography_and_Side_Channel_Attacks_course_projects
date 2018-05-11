% hw3.3 by MSI
clear all;
clc;

% part a of the question 3
tic

% i use the following table for precalculated hamming weight values
% using a lookup table is much faster than calling a function and
% actually calculating the values. since inputs are always 1 byte,
% i don't need to worry about out of index values

hwtable = [0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,4,5,5,6,5,6,6,7,5,6,6,7,6,7,7,8];

fid = fopen('PowerTrace.dat');
fid2 = fopen('Plaintext.dat');
trace = zeros(500,30000);
plaintext = zeros(500,1);
secretkey = zeros(1,16);
for i=1:500
    trace(i,:) = fread(fid, 30000, 'uint8');
    temp_pt = fread(fid2, 16, 'uint8');
    plaintext(i,1:16) = temp_pt(1:16,1);
end

%% mean and variance calculations

% tracemean = zeros(1,30000);
% tracevar = zeros(1,30000);

% calculating mean and variance over time for the power trace data
% for i=1:30000
%     tracemean(i) = mean(trace(:,i)); % mean over time
%     tracevar(i) = var(trace(:,i)); % variance over time
% end
%     plot(tracemean);title('Mean value for each trace sample');
%     figure;plot(tracevar);title('Variance value for each trace sample');
      
for byte_no = 1:16
    ptbyte = plaintext(:,byte_no);
    

    % addbox function takes x,k inputs and calculates the addkey+sbox
    y = zeros(500,256);

    % calculating all hypothetical intermediate values y (500x256) for the
    % first byte of the plaintext data
    ymean = zeros(1,256);yvar=zeros(1,256);
%     str = 'calculating y values for byte ';
%     bno = num2str(byte_no);
%     str = strcat(str,' ', bno);
%     display(str); 

    % part b of the question 3

    for key=1:256
        for i=1:500        
            y(i,key) = addbox(ptbyte(i),key-1);
        end
        ymean(key) = mean(y(:,key)); % mean for all possible key
        yvar(key) = var(y(:,key)); %
    end
%     display('y calculation for all possible keys is completed'); 
    
%     plot(ymean);title('Sample Mean for each key candidate');
%     figure;plot(yvar);title('Sample Variance value for each key candidate');
    
%% hamming weight correlation method
    hwy = zeros(500,256);
    for i=1:500
        for j=1:256
            hwy(i,j) = hwtable(y(i,j)+1);
        end
    end
    
    correlation = corr(trace,hwy);
    max_cor = zeros(1,256);
    for i=1:256
        max_cor(i) = max(correlation(:,i));
    end
     
%% LSB correlation method
%     lsby = zeros(500,256);
%     for i=1:500
%         for j=1:256
%             lsby(i,j) = mod(y(i,j),2);
%         end
%     end
%     
%     correlation = corr(trace,lsby);
%     max_cor = zeros(1,256);
%     for i=1:256
%         max_cor(i) = max(correlation(:,i));
%     end
    
%% MSB correlation method
%     msby = zeros(500,256);
%     for i=1:500
%         for j=1:256
%             msby(i,j) = floor((y(i,j)/128));
%         end
%     end
%     
%     correlation = corr(trace,msby);
%     max_cor = zeros(1,256);
%     for i=1:256
%         max_cor(i) = max(correlation(:,i));
%     end
    
    %%
    [val, index] = max(max_cor);
    secretkey(byte_no)=index;
    idx = dec2hex(index);
    
%     temp = byte_no;
%     str = ['Key byte %d', temp,' is ', idx];
%     display(str);
% 
%     figure;plot(max_cor);title(str);

%%%%%%%%%%%%%%%
%% PLOT SECTION

    % plotting the correlation for each key
%     for i=1:256
%        hold on;
%        if i==index
%            plot(correlation(:,i),'red');
%        else
%        plot(correlation(:,i));title('trace correlations');
% %        pause(0.2);
%        end
%     end
%%
   display(['key byte ',num2str(byte_no),' is found!']);
   
end

x= ['secret key is ', num2str(secretkey),'\n','in hexadecimal; ' ];
disp(x)
dec2hex(secretkey)

toc

