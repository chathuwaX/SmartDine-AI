import React, { useState, useEffect } from 'react';
import { fetchMenu } from '../api';
import { Loader2 } from 'lucide-react';

export default function Menu() {
    const [menuItems, setMenuItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const loadMenu = async () => {
            try {
                const data = await fetchMenu();
                setMenuItems(data);
            } catch (err) {
                setError('Failed to load menu. Is the backend running?');
            } finally {
                setLoading(false);
            }
        };
        loadMenu();
    }, []);

    if (loading) return <div className="flex justify-center mt-20"><Loader2 className="animate-spin text-orange-600" size={40} /></div>;
    if (error) return <div className="text-center text-red-500 mt-20">{error}</div>;

    const categories = [...new Set(menuItems.map(item => item.category))];

    return (
        <div>
            <h2 className="text-3xl font-bold mb-8 text-center">Our Menu</h2>
            {categories.map(category => (
                <div key={category} className="mb-12">
                    <h3 className="text-2xl font-semibold mb-6 border-b pb-2">{category}</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {menuItems.filter(item => item.category === category).map(item => (
                            <div key={item.id} className="bg-white rounded-xl shadow-sm border overflow-hidden hover:shadow-md transition">
                                {item.image_url ? (
                                    <img src={item.image_url} alt={item.name} className="h-40 w-full object-cover" />
                                ) : (
                                    <div className="h-40 bg-gray-200 flex items-center justify-center">
                                        <span className="text-gray-400">Image Placeholder</span>
                                    </div>
                                )}
                                <div className="p-5">
                                    <div className="flex justify-between items-start mb-2">
                                        <h4 className="font-bold text-lg">{item.name}</h4>
                                        <span className="font-bold text-orange-600 shrink-0">Rs. {item.price}</span>
                                    </div>
                                    <p className="text-gray-600 text-sm mb-4">{item.description}</p>
                                    <div className="flex justify-between items-center">
                                        {item.vegetarian && (
                                            <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded font-medium">Vegetarian</span>
                                        )}
                                        {!item.vegetarian && <span></span>}
                                        <button className="text-orange-600 font-medium text-sm hover:underline">Add to order</button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
}
