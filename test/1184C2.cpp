#include <iostream>
using namespace std;
typedef long long int ll;
 
ll N;
ll A[100005];
ll ans;
 
int main(){
	cin>>N;
	for(int i=0;i<N;i++){
		cin>>A[i];
		ans-=A[i];
	}
	for(int i=1;i<N;i++)
		A[i]=max(A[i-1],A[i]);
	for(int i=N-2;i>=0;i--)
		A[i]=max(A[i],A[i+1]-1);
	for(int i=0;i<N;i++)
		ans+=A[i];
	cout<<ans;
}