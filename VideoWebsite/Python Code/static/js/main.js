var app=new Vue({
  el: '#app',
  data () {
    return {
      info: null,
      videos: '',
      username: '',
      password: '',
      error: false,
      userInfo: null,
      responseMessage: '',
      handle: null,
      usern: null,
      newHandle: '',
      image: '',
      file: '',
      newTitle: '',
      files: [],
      fileToPlay: '',
    }
  },

  methods: {
    submitFile(event){
      let formData = new FormData();
      formData.append('file', this.file);
      axios.post( 'https://info3103.cs.unb.ca:50533/users/'+this.username+'/videos/upload',
          formData,
          {
          headers: {
              'Content-Type': 'multipart/form-data'
          }
        }
      ).then(function(){
        console.log('SUCCESS!!');
      })
      .catch(function(){
        console.log('FAILURE!!');
      });
    },

    handleFileUpload(){
      this.file = this.$refs.file.files[0];
    },

    loadUsers: function (event) {
      axios.get('https://info3103.cs.unb.ca:50533/users', {withCredentials:true},)
        .then(response => (this.info = response.data.Users))
        .catch(function(error){
              console.log(error)
        });
    },

    loadUser: function (event, handle) {
      axios.get('https://info3103.cs.unb.ca:50533/users/'+handle, {withCredentials:true},)
        .then(response => (this.userInfo = response.data.User))
        .catch(function(error){
              console.log(error)
        });
    },

    loadVideos: function (event) {
      axios.get('https://info3103.cs.unb.ca:50533/videos', {withCredentials:true},)
        .then(response => (this.videos = response.data))
        .catch(function(error){
              console.log(error)
        });
    },

    playVideo: function (event, file) {
      this.$refs.videoRef.src = file;
      this.$refs.videoRef.play();
    },

    loadVideo: function (event, fileName) {
      // axios.get('https://info3103.cs.unb.ca:50533/static/Uploads/'+fileName, {withCredentials:true})
      // .then(response => ())
      // .catch();
      // console.log(document.getElementById("video").src);
      // // /static/Uploads/{{video.fileName}}
      // var videoPath = document.getElementById("video").src;
      // videoPath = "/static/Uploads/"+fileName;
      // console.log('hello');
      // console.log(videoPath);
    },

    aUserPage: function(){
      var addUsers = document.getElementById("addUsersDiv");
      addUsers.style.display = "block";
    },

    adduser: function(event){
      var postData = {
          username : this.usern,
          handle : this.handle
      };
      let axiosConfig = {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            "Access-Control-Allow-Origin": "*",
          },
      };
      axios.post('https://info3103.cs.unb.ca:50533/users',
              postData,
              axiosConfig)
          .then(function (response) {
            //disable the signin display if the sign in was successful
            if(response.status == 201){
              var checkuser = document.getElementById("checkUser");
              checkuser.innerHTML = "User added";
              var addUsers = document.getElementById("addUsersDiv");
              addUsers.style.display = "block";
            }
          })
          .catch(function (error) {
            console.log(error);
          })

    },

    updateUser: function(event, handle) {
      var postData = {
          newHandle : this.newHandle,
      };
      let axiosConfig = {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            "Access-Control-Allow-Origin": "*",
          },
      };
      axios.put('https://info3103.cs.unb.ca:50533/users/'+handle,
        postData,
        axiosConfig)
      .then(response => (this.responseMessage = response.data))
      .catch(function (error) {
        console.log(error);
      });
      this.newHandle = '';
    },

    updateVideo: function(event, title) {
      var postData = {
          newTitle : this.newTitle,
      };
      let axiosConfig = {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            "Access-Control-Allow-Origin": "*",
          },
      };
      axios.put('https://info3103.cs.unb.ca:50533/users/'+this.username+'/videos/'+title+'/edit',
        postData,
        axiosConfig)
      .then(response => (this.responseMessage = response.data))
      .catch(function (error) {
        console.log(error);
      });
      this.newTitle = '';
    },

    deleteUser: function(event, handle) {
      axios.delete('https://info3103.cs.unb.ca:50533/users/'+handle, {withCredentials:true},)
      .then(response => (this.responseMessage = response.data))
      .catch(function(error) {
        console.log(error);
      });
      alert("Deleted User"+this.responseMessage);
    },

    deleteVideo: function(event, title) {
      axios.delete('https://info3103.cs.unb.ca:50533/users/'+this.username+'/videos/'+title+'/edit', {withCredentials:true})
      .then(response => (this.responseMessage = response.data))
      .catch(function(error) {
        console.log(error);
        alert("That is not your video!");
      });
    },

    loginLoad: function (event) {
      axios.get('https://info3103.cs.unb.ca:50533/signin', {withCredentials:true},)
        .then(function(response){
          console.log(response);
        })
        .catch(function(error){
              console.log(error)
        });
    },

    logout: function () {
      axios.delete('https://info3103.cs.unb.ca:50533/signin')
      .then(function (response) {
        if(response.status == 200){
          location.replace("https://info3103.cs.unb.ca:50533");
          var lgnPage = document.getElementById("loginPage");
          lgnPage.style.display = "block";
          alert("Logged Out");
        }
      })
      .catch(function (error) {
        console.log(error);
      });
    },

    login: function (event) {
      var postData = {
          username : this.username,
          password : this.password
      };
      let axiosConfig = {
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            "Access-Control-Allow-Origin": "*",
          },
      };
      axios.post('https://info3103.cs.unb.ca:50533/signin',
              postData,
              axiosConfig)
          .then(function (response) {
            //disable the signin display if the sign in was successful
            if(response.status == 201){
              var lgnPage = document.getElementById("loginPage");
              var notLogin = document.getElementById("addUsersDiv");
              var footerUser = document.getElementById("displayUser");
              notLogin.style.display = "block";
              lgnPage.style.display = "none";
              var usnam = response.config.data;
              footerUser.innerHTML = "<p>Hello " + usnam.split('\"')[3]; + "</p>";
            }
          })
          .catch(function (error) {
            var footerUser = document.getElementById("displayUser");
            footerUser.innerHTML = "Incorrect Credentials";
            console.log(error);
          })
    },
  }
})
