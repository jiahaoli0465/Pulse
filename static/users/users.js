document.addEventListener('DOMContentLoaded', () => {
    const userActions = document.querySelectorAll('.user-action');

    const handleFollow = async (e, form) => {
        e.preventDefault();
        const userId = form.getAttribute('data-userid');
        const response = await axios.post(`/api/users/${userId}/follow`);

        if (response.data.status === 'success') {
            const newFormHtml = `<form method="POST" class="unfollowForm" data-userid="${userId}" action="">
                                    <button type="submit" class="action-button unfollow">Unfollow</button>
                                 </form>`;
            form.outerHTML = newFormHtml;
            document.querySelector(`.unfollowForm[data-userid="${userId}"]`).addEventListener('submit', e => handleUnfollow(e, e.currentTarget));
        }
    };

    const handleUnfollow = async (e, form) => {
        e.preventDefault();
        const userId = form.getAttribute('data-userid');
        const response = await axios.post(`/api/users/${userId}/unfollow`);

        if (response.data.status === 'success') {
            const newFormHtml = `<form method="POST" class="followForm" data-userid="${userId}" action="">
                                    <button type="submit" class="action-button follow">Follow</button>
                                 </form>`;
            form.outerHTML = newFormHtml;
            document.querySelector(`.followForm[data-userid="${userId}"]`).addEventListener('submit', e => handleFollow(e, e.currentTarget));
        }
    };

    userActions.forEach(action => {
        const followForm = action.querySelector('.followForm');
        const unfollowForm = action.querySelector('.unfollowForm');

        if (followForm) {
            followForm.addEventListener('submit', e => handleFollow(e, followForm));
        }

        if (unfollowForm) {
            unfollowForm.addEventListener('submit', e => handleUnfollow(e, unfollowForm));
        }
    });
});
