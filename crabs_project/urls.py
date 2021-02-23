import crabs_project.views as views


router = {
    '/': views.IndexPage(),
    '/second/': views.non_index,
    '/participate/': views.participate,
    '/courses/': views.courses,
    '/professions/': views.professions,

}

