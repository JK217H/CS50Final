import { ref } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';

const projecttags = ref([]);
const toast = useToast();

// checks for duplicates
const checkDupl = (tag) => {
  // fix loop syntax 
  for(let i = 0; i < projecttags.length; i++ ) {
  if (projecttags[i] == tag)
    return false;
}
}
// gets all the tags 
const fetchTags = async () => {
  try {
    const res = await axios.get(`http://localhost:5000/project-tags`);
    projecttags.value = res.data;
  } catch (error) {
    toast.error('Failed to load projecttags');
      console.error(error)
  }
};

const addTag = (tag) => {
  fetchTags();
  if (checkDupl(tag) == false ){
    alert("Tag already exists")
  }
  else {
    handleValid(tag);
  }
};

const handleValid = async (tag) => { 
  const newTag = {
    tag: tag,
  };
  try {
    const res = await axios.post(`http://localhost:5000/project-tag`, newTag)
    toast.success('Tag added succesfully')
  } catch(error) {
    console.error(error);
    toast.error('Failed to add tag')
  }

}

export function useProjectTags() {
  return { projecttags, addTag, fetchTags };
}