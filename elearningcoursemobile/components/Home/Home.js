import { ActivityIndicator, FlatList, Image, Text, TouchableOpacity, View } from "react-native"
import MyStyles from "../../styles/MyStyles";
import { useEffect, useState } from "react";
import { Chip, List, Searchbar } from "react-native-paper";
import Apis, { endpoints } from "../../configs/Apis";

const Home = () => {
    const [categories, setCategories] = useState([]);
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState([false]);
    const [kw, setKw] = useState("");
    const [page, setPage] = useState(1);
    const [cateId, setCateId] = useState(null);

    const loadCate = async () => {
        let res = await Apis.get(endpoints['categories']);
        setCategories(res.data);
    }

    const loadCourses = async () => {
        if (page > 0) {
            try {
                setLoading(true)
                let url = `${endpoints["courses"]}?page=${page}`;
                if (kw) {
                    url = `${url}&q=${kw}`
                }

                if (cateId) {
                    url = `${url}&category_id=${cateId}`
                }

                let res = await Apis.get(url);
                setCourses([...courses, ...res.data.results]);
                if (res.data.results === null)
                    setPage(0);
            }
            catch {

            }
            finally {
                setLoading(false)
            }
        }
    }

    useEffect(() => {
        loadCate();
    }, []);

    useEffect(() => {
        let timer = setTimeout(() => {
            loadCourses();
        }, 500);

        return () => clearTimeout(timer);
    }, [kw, page, cateId]);

    const loadMore = () => {
        if (!loading && page > 0) {
            setPage(page + 1);
        }
    }

    /*Đặt lại giá trị của page là 1 khi tìm kiếm,...*/
    const search = (value, callback) => {
        setPage(1);
        callback(value);
        setCourses([])
    }

    return (
        <View style={MyStyles.container}>
            <Text style={MyStyles.subject}>E-Course</Text>

            <View style={[MyStyles.row, MyStyles.warp]}>
                <TouchableOpacity key={c.id} onPress={() => search(null, setCateId)}>
                    <Chip style={MyStyles.m5}>Tất cả</Chip>
                </TouchableOpacity>
                {categories.map(c => <TouchableOpacity key={c.id} onPress={() => search(c.id, setCateId)}>
                    <Chip style={MyStyles.m5}>{c.name}</Chip>
                </TouchableOpacity>
                )}
            </View>

            <Searchbar placeholder="Tìm kiếm khóa học" value={kw} onChangeText={t => search(t, setKw)} />

            {loading && <ActivityIndicator />}
            <FlatList onEndReached={loadMore} data={courses} renderItem={({ item }) => <List.Item key={item.id} title={item.subject} description={item.created_date} left={() => <Image style={MyStyles.avatar} source={{ uri: item.image }} />} />} />

        </View>
    )
}

export default Home;