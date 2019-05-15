var intro = introJs();
intro.setOptions(
    {
        steps: [
            {
                intro: "<div style='text-align: center'>Welcome to <b>OpenROAD</b> Cloud Flow!</div>"
            },
            {
                element: document.querySelector('#intro-dashboard'),
                intro: "The dashboard gives you quick numbers on your designs and the flows being run on them."
            },
            {
                element: document.querySelector('#intro-live-monitor'),
                intro: "When your flows are running on our cloud platform, the live monitor shows you live progress of the flow."
            },
            {
                element: document.querySelector('#intro-notification-panel'),
                intro: "Important notifications on your account and flows are shown here. Just click on any of them to navigate to the corresponding page in the website."
            },
            {
                element: document.querySelector('#intro-navigation'),
                intro: "Tha navigation side panel gives you quick access to important functionality of the platform. Now, click on <i>My Designs</i> to import your first design.",
                position: 'right'
            }
        ],
        exitOnEsc: true,
        showStepNumbers: true
    }
);
intro.start();
