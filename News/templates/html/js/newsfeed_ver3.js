var address='http://localhost:8000';

function post_data(url ,postBody){
    axios
    .post(url, postBody)
      .then(function (response) {
        console.log(response);
    })
    .catch(error => {
        console.log(error)
    })
}
var News = new Vue({
    el:"#delewith",
    data: {
        editNews:'',
        my:{
            userID:11,
            Nick:"zydoooog"
        },
        myID:11,
        hostadd:address,
        items:[]
    },
    mounted(){
        console.log(this.myID);
        var url=this.hostadd+'/News/getFriendNews/';
        axios
            .get(url,{withCredentials:true})
            .then(response => {
                console.log(response.data);
                if(response.data.error==false){
                    News.items = response.data.data;
                }
            })
            .catch(error => {
                console.log(error)
                this.errored = true
            })
            .finally(() => this.loading = false);
    },
    methods:{
        like(item) {
            var url=this.hostadd+'/News/likeOperate/';
            var PostData={
                newsID:item.News.newsID,
                op:item.News.liked?'add':'delete'
            }
            axios
                .post(url,JSON.stringify(PostData))
                .then(response => {
                    if(response.data.error==false){
                        item.News.cntlike+=item.News.liked?-1:1;
                        item.News.liked=!item.News.liked;
                    }
                })
                .catch(error => {
                    console.log(error)
                    this.errored = true
                })
        },
        add_comment(item ,content) {
            url=this.hostadd+'/News/commentOperate/'
            var res={
                userID:this.my.userID,
                Nick:this.my.Nick,
                commentID:0,
                content:content
            }
            var postBody={
                op:'add',
                content:content,
                newsID:item.News.newsID
            };
            axios
            .post(url, JSON.stringify(postBody))
              .then(function (response) {
                console.log(response.data);
                if(response.data.error==false){
                    res.commentID=response.data.data.newsID;
                    item.News.comment.push(res);
                }
            })
            .catch(error => {
                console.log(error)
            })
        },
        del_comment(item ,index) {
            url=this.hostadd+"/News/commentOperate/";
            var postBody={
                op:'delete',
                commentID:item[index].commentID
            };
            axios
            .post(url, JSON.stringify(postBody))
            .then(function (response) {
                console.log(response.data);
                if(response.data.error==false){
                    item.splice(index,1);
                }
            })
            .catch(error => {
                console.log(error)
            })
        },
        add_news(content){
            var res={
            user:{
                userID:this.my.userID,
                Nick:this.my.Nick
            },
            News:{
                newsID:undefined,
                content:content,
                cntlike:0,
                liked:false,
                comment:[],
                date:new Date()
            }};
            
            url=this.hostadd+"/News/newsOperate/";
            var postBody={
                content:'',
                op:'add'
            };
            postBody.content=content;
            axios
            .post(url, JSON.stringify(postBody))
            .then(function (response) {
                console.log(response.data);
                if(response.data.error==false){
                    res.News.newsID=response.data.data.newsID;
                    News.items.push(res);
                }
            })
            .catch(error => {
                console.log(error)
            })
            

        },
        del_news(index){
            url=this.hostadd+"/News/newsOperate/";
            var ID=this.items[index]
            console.log(ID);
            var postBody={
                op:'delete',
                newsID:this.items[index].News.newsID
            };
            axios
            .post(url, JSON.stringify(postBody))
            .then(function (response) {
                console.log(response.data);
                if(response.data.error==false){
                    News.items.splice(index,1);
                }
            })
            .catch(error => {
                console.log(error)
            })
            
        }
    }
});

