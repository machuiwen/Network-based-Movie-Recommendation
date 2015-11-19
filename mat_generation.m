clear;
%%
load userEdge_1M.txt
disp('load done');
S = spconvert(userEdge_1M);
user_similarity_matrix = full(S);
% clear S userEdge_1M
%%
user_similarity_matrix = [user_similarity_matrix; zeros(1, size(user_similarity_matrix,2))];
user_similarity_matrix = user_similarity_matrix + user_similarity_matrix';
user_similarity_matrix = user_similarity_matrix + eye(size(user_similarity_matrix, 1));
%%
save('user_similarity_matrix.mat', 'user_similarity_matrix')

%%
clear;
load movieEdge_1M.txt
disp('load done');
S = spconvert(movieEdge_1M);
movie_similarity_matrix = full(S);
% clear S movieEdge_1M
movie_similarity_matrix = [movie_similarity_matrix; zeros(1, size(movie_similarity_matrix,2))];
movie_similarity_matrix = movie_similarity_matrix + movie_similarity_matrix';
movie_similarity_matrix = movie_similarity_matrix + eye(size(movie_similarity_matrix, 1));
save('movie_similarity_matrix.mat', 'movie_similarity_matrix')