import type { NextPage } from "next";
import dynamic from "next/dynamic";

const Home: NextPage = () => {
  const Map = dynamic(() => import("../components/Map"), { ssr: false });
  return <Map />;
};

export default Home;
