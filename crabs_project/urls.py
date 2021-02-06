import crabs_project.views as views


router = {
    '/': views.index,
    '/second/': views.non_index,
    '/form/': views.form,
}

