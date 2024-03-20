const preStory = () => {
    const activeElement = $(".eachSlide.active").index();
    activeElement != 0 && changeStory(activeElement - 1);
  };
  const nextStory = () => {
    const activeElement = $(".eachSlide.active").index();
    const maxCount = $("#progressBar .eachSlide").length;
    activeElement != maxCount - 1 && changeStory(activeElement + 1);
  };
  const changeStory = (index) => {
    $(".storiesContainer .eachStory video").trigger("pause");
    const videoPositionSet = document.querySelector(".eachStory.active video");
    if (videoPositionSet != null) {
      videoPositionSet.currentTime = 0;
    }
  
    $("#progressBar .eachSlide").removeClass("active");
    $(".storiesContainer .eachStory").removeClass("active");
  
    $("#progressBar").children().eq(index).addClass("active");
    $(".storiesContainer").children().eq(index).addClass("active");
    $(".storiesContainer .eachStory.active video").trigger("play");
  };
  
  const storyNavigateShare = () => {
    if (navigator.share) {
      navigator.share({
        title: document.title,
        text: "Hello World",
        url: window.location.href
      });
      // .then(() => console.log('Successful share'))
      // .catch(error => console.log('Error sharing:', error));
    }
  };
  