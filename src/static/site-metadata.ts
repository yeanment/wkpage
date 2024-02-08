interface ISiteMetadataResult {
  siteTitle: string;
  siteUrl: string;
  description: string;
  keywords: string;
  logo: string;
  navLinks: {
    name: string;
    url: string;
  }[];
}

const data: ISiteMetadataResult = {
  siteTitle: 'Workouts Map',
  siteUrl: 'https://yeanment.github.io',
  logo: 'https://avatars.githubusercontent.com/u/38305958?v=4',
  description: 'Personal site and blog',
  keywords: 'workouts, running, cycling, riding, roadtrip, hiking, swimming',
  navLinks: [
    {
      name: 'Blog',
      url: 'https://yeanment.github.io',
    },
    {
      name: 'About',
      url: 'https://github.com/yeanment/wkpage/blob/master/README-CN.md',
    },
  ],
};

export default data;
